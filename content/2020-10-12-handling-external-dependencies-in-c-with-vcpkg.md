---
title: Handling external dependencies in C/C++ with Vcpkg
date: 2020-10-12
tags: c++, c, build, cmake, native, programming
slug: handling-external-dependencies-in-cplusplus-with-vcpkg
---

If you had been developing software for a while, you already know the advantages of using a good package manager for your dependencies, every Javascript developer knows about [npm](https://npmjs.com), Java developers have [Maven](https://maven.apache.org) and .Net developers (last time I checked) still use [Nuget](https://www.nuget.org/), what about C/C++ developers? how do we handle external libraries and dependencies?

Well, in the native world of C/C++ things are a little different (mostly because historical reasons). C/C++ are a different "beast" and there are many factors and reasons it is really hard to develop a standard and common package manager for them because you have to deal with a library or libraries that have different settings and configurations for different operating systems, architectures, release types and even compilers! (yes, while we have standards compilers sometimes add specific extensions that are not compatible between them, generating different binaries). It is not as easy as just download the package and their dependencies and that is all, you have to deal with a lot of other factors when compiling a C/C++ program, hence the difficulty of creating a common, easy to use and compatible package manager.

That does not mean we had not tried, there are out there a plethora of package manager attempts in the C/C++ world (as many as build systems) and some of them have more success than others. One I recently discovered and started using is [vcpkg](https://github.com/microsoft/vcpkg), by Microsoft, a multiplatform and open source package manager designed with versatility in mind. I struggled a little when starting learning how to use it so I decided to write a simple post about using it from scratch so I don't forget next time I need it.

# Installation

This is, in my opinion, the first big pain point in using Vcpkg, there is no simple installer, no [Chocolatey](https://chocolatey.org) or [Scoop](https://scoop.sh) in Windows or any [Homebrew](https://brew.sh/) recipe in macOS (and yes, before you ask, no packages for Linux distros). The "way" you have to install Vcpkg is the "old way", you have to clone the repository and set its path in your executable path to use it... Yes, the problem it promises to solve is not really a problem they solved for themselves...

 - First we clone the repository: `git clone https://github.com/microsoft/vcpkg.git d:\code\vcpkg`
 - Now we need to _build_ the tool for our OS, yes, after all you are going to do C/C++ development in your machine!
 - There is a bootstrap script (`bootstrap-vcpkg.bat` or `bootstrap-vcpkg.sh` if you are in Windows or macOS/Linux). The script will tell you if you need to install any required dependency
 - Now that the building for the tool finished, you need to add it to your executable path, do this as you are used to in your operating system, I am pretty sure I don't have to tell you how to do this if you are reading this blog post
 - The previous step is very important, somehow vcpkg depends and assume it is in your executable path. I had tried using temporary paths and path replacement and it simple does not work!

# Using dependencies

Let's do something simple. I use [JSON](https://en.wikipedia.org/wiki/JSON) in a fair amount at my work, so let's do a simple program using the popular [nlohmann/json](https://github.com/nlohmann/json) library for parsing it in C++, it will be a simple C++ program (you can try with plain C and your favourite JSON library as well):

```c++
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
        auto entry = json::parse("{ \"name\": \"cristian\" }");
        std::cout << "His name is: " << entry["name"] << "\n";
}
```

As you see, nothing really complicated, just a simple program to show how to use _any_ other external library. Now let's search for the JSON library in `vcpkg` using the `search` command:

```bash
vcpkg search nlohmann
```

We found the library in VCPKG:

```
json-schema-valid... 2.1.0            This is a C++ library for validating JSON documents based on a JSON Schema. Th...
nlohmann-fifo-map    2018.05.07-1     a FIFO-ordered associative container for C++
nlohmann-json        3.9.1            JSON for Modern C++
```

It is time to install it, we do this with the `install` command:

```bash
vcpkg install nlohmann-json
```

If you look at the bottom, after installing the package you will see the following message:

```bash
The package nlohmann-json:x86-windows provides CMake targets:

    find_package(nlohmann_json CONFIG REQUIRED)
    target_link_libraries(main PRIVATE nlohmann_json nlohmann_json::nlohmann_json)
```

And that will be all... Not really, now we need to write our [CMake](https://cprieto.com/tag/cmake.html) build file (`CMakeLists.txt`) and add those lines for our dependencies:

```cmake
cmake_minimum_required (VERSION 3.10)
project (sample)

find_package (nlohmann_json CONFIG REQUIRED)

add_executable (main main.cpp)
target_link_library (main PRIVATE nlohmann_json nlohmann_json::nlohmann_json)
```

And now it is time to build, as usual, let's do an _out-of-source_ build with CMake, but this time, we need to pass the path for the special file `vcpkg.cmake` coming in the vcpkg _installation_ directory:

```bash
mkdir build && cd build
cmake .. "-DCMAKE_TOOLCHAIN_FILE=d:\code\vcpkg\scripts\buildsystems\vcpkg.cmake"
cmake --build . --clean-first
```

If you did the previous steps in a macOS or Linux machine (or in a Windows 32 machine) you will have the `main` executable build and ready to run, but in Windows 64 it will tell you the package is not there or something regarding not finding the package nlohmann_json (the package you needed to install)... What is happening? I thought this was cross platform?

## The problem building in Windows

Well, it is not in their tutorial but I found the problem is the platform you compiled Vcpkg in Windows, by default it is compiled for 32 bit architecture in Windows and _every package_ you install will be installed for that platform. If you try to compile the previous example telling CMake to use 32 bit instead of 64 bit (using Visual Studio 2019) it will just work:

```bash
cmake .. "-DCMAKE_TOOLCHAIN_FILE=d:\code\vcpkg\scripts\buildsystems\vcpkg.cmake" -A Win32
```

What if I want the library and executable as a 64 bit application? well, you just have to tell to Vcpkg that you need to install the 64 bit of the library instead of whatever it decides to install, this platform specification is for more than just your CPU architecture but includes the compiler, operating system and type of library (static/dynamic). You can see the supported triplets using `vcpkg help triplets`. Meanwhile we just tell to Vcpkg to install the Win64 library for nlohmann/json for our example:

```bash
vcpkg install nlohman-json:x64-windows
```

Now we can compile as both 32 and 64 bit just passing the correct parameter to CMake and it won't fail!

If you write code in Windows and you are going to develop applications _only_ for 64 Windows then you can pass the parameter `win64` when building Vcpkg (in the bootstrap script):

```bash
bootstrap-vcpkg.bat -win64
```

And now it will fetch the x64-windows triplet by default when installing any libraries.

**UPDATE**: This actually does not work and it doesn't matter if Vcpkg is compiled for x64 in Windows. By default, in Windows, the build architecture will be _always_ x86 and if you want to install a package for x64 you have to always specify the architecture triplet in the name or using the `--triplet` parameter. Another option is using the environment variable `VCPKG_DEFAULT_TRIPLET=x64-windows` to tell to Vcpkg to always use x64, go figure! There is [a closed issue](https://github.com/microsoft/vcpkg/issues/1254) with this problem.

# Is that all?

Well, not really, there are many additional commands and use cases for Vcpkg, it is pretty mature and widely used and more libraries are constantly added to the repertoire. The documentation is _ok_ and while is made by Microsoft it is clearly not centered around the Microsoft world. I really wish their setup and installation use cases feel a little less "hacky" but I see a lot of improvements in the tooling.

Is this the only package manager I should use for C/C++? not really, in big projects you will probably end up with a mix of them. There is another really good package manager out there, [Conan](https://conan.io/), but I will talk about it and how to use it in another blog post in the near future.
