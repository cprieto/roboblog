---
title: Handling external dependencies in C/C++ with Conan
date: 2020-10-26
tags: c++, c, build, cmake, native, programming
slug: handling-external-dependencies-in-cplusplus-with-conan
---

Last time we saw how to handle [dependencies with vcpkg]({filename}/2020-10-12-handling-external-dependencies-in-c-with-vcpkg.md), an open source, cross platform package made by Microsoft trying to solve the external dependencies problem with native code. Vcpkg solves the problem in a centralized way, if you don't see a package you want to use, you ask in the issue tracker or make a PR with a patch, cmake file and required files to make the package work in the application build. Everything is in the same directory and repository (see the `/ports` directory) and that is why you need to update your repository and vcpkg application once in a while if you want updates.

[Conan](https://conan.io) is another popular cross platform package manager for C/C++, its approach is slightly different. In Conan, the developer has complete control of the package creation and build packages are available (so you don't have to build the package from scratch just to use it). Maybe the best way to explain the difference is doing the same example as last time but now with Conan.

First, let's install Conan, it is a Python application so you need Python installed in your machine. The [instructions]() in the official page are clear but in my case, I installed it using [Homebrew](https://brew.sh/) in my macOS and [Scoop](https://scoop.sh/) in Windows and the `pip` method in Linux. Just follow the instructions, it is that easy.

Ok, let's say you already have installed conan and we want to compile the same project as the last time, a simple program using the [nlohman json](https://github.com/nlohmann/json) library:

```c++
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
        auto entry = json::parse("{ \"name\": \"cristian\" }");
        std::cout << "His name is: " << entry["name"] << "\n";
}
```

We need to understand that Conan is a meta package generator, pretty much like what CMake is for building. You not only specify the library requirements but the conditions for the build and what are you going to use to build it. To understand this let's solve the first problem, the JSON library requirement. Conan depends on what they call a remote repository that is a central server with package information, think about the remote repository server in [npm](https://npmjs.com), you can have multiple repositories and host your own company repository as well. By default Conan installs the [Conan Center](https://conan.io/center/) repository. For search for any package containing the word "json" in its name we can issue the command:

```
conan search "*json" -r conan-center
```

I found this way to find packages _extremely slow_ so instead I go to the [Conan Center](https://conan.io/center/) search page and do it there.

We see the package we need is named `nlohman_json` and the latest version is `3.9.1`, we now create a file `conanfile.txt` with the _requirements_ and _how are we going to build it_ (this last part is required for conan to specify a way to include the libraries):

```ini
[requirements]
nlohmann_json/3.9.1

[generators]
cmake
```

We specify [CMake](https://cmake.org) as our build generator. There are _plenty_ of different generators and we can specify multiple generators for the same build. In fact, there are generators where they even download and run the whole build system so you only need Conan installed in your machine. You can check the list of available generators in the [Conan documentation](https://docs.conan.io/en/latest/reference/generators.html).

Now it is time to work in our build script. This will be _very similar_ to the previous build but with a very small change:

```cmake
cmake_minimum_required (VERSION 3.10)
project (sample)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable (main main.cpp)
target_link_library (main ${CONAN_LIBS})
```

Notice the line including a file that conan will _generate_ for us, this file contains macros and specifications for our build files then we tell this set of macros to do the required setup and do the dependency walk. Later to link our dependencies we use the variable `${CONAN_LIBS}` in the linkage step.

With this is enough to run the following commands in an out-of-source build:

```
mkdir build
cd build
conan install ..
cmake ..
cmake --build . --clean-first
```

It is important to run `conan install` _before_ running CMake, this will generate the required `conanbuildinfo.cmake` file and prepare the dependencies. We don't need to specify an toolchain file like with Vcpkg.

Conan is _extremely flexible_ and powerful, and on top of that, their documentation is amazing (just go and check the [official Conan documentation](https://docs.conan.io/en/latest/introduction.html)) and they even include videos and seminars about using Conan from basic users to expert applications.

When developing C/C++ applications, Conan is always my first choice and I use Vcpkg only if there are not other option. The developers are working in version 2.0 where a new world of options for dependency handling will be opened for C++ developers. Go and give it a try, you won't regret it!
