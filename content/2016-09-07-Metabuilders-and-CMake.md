---
title: Metabuilders and CMake
date: 2016-09-07
tags: cmake, build, programming
---

Most of us are already exposed of familiar with build systems like [MSBuild](https://en.wikipedia.org/wiki/MSBuild) or [Make](https://www.gnu.org/software/make/) and well, we already know how difficult it is to maintain really huge basecodes or crafting really big msbuild or Makefiles, and then, add targetting multiple platforms for a native developer!

Enter the meta build systems.

Basically what they do is to describe what we want to build and then from that it generates a native build script using [Makefile](http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/) or [Ninja](https://ninja-build.org/) or MSBuild or even a project file for your IDE!

There are a few meta build systems out there, and [CMake](https://cmake.org/) is one of them. I am writing this as a reminder of how easy is to start with CMake and the awesome things you can do with it.

# Hello world

We need a simple source code for this, assuming the file name is `hello.c`:

```c
#include <stdio.h>

int main() {
    printf("hello world\n");
}
```

Well, the simplest `CMakeLists.txt` file for this would be something like this:

```cmake
add_executable (hello hello.c)
```

Now, let's tell to CMake to do the magic for us, let's run this in the command line:

    cmake .

If you are running in macOS or Linux, with Make installed, you will find... a `Makefile`! (or if you are running in Windows with Visual Studio installed you will find a Visual studio solution named `Project.sln` or something like that). Let's assume you are using Make, so to compile just run make:

    make

Done. You will be able to run our hello world application!

# Extending the sample

Well, if you check the output from `CMake` you will find a weird warning about the required version. This is because with every version of CMake they introduce new commands and things like that, so it is a good idea to tell to whoever is building the script what is the minimum required version of CMake to build this app, it is a simple command and it costs nothing. In my case my current version of CMake is 3.6.1, let's say the minimum required is 3.6:

```cmake
cmake_minimum_required (VERSION 3.6)
add_executable (hello hello.c)
```
As I mentioned before, if you do this in Windows you will get a `Project.sln` file, that is not good, we want to give to our project an awesome name. Let's do that:

```cmake
cmake_minimum_required (VERSION 3.6)
project (HelloCMake)
add_executable (hello hello.c)
```
And that is the simplest zero warning CMake file we can do!

# Libraries

Let's make a simple library, starting with the header file, let's call this file `greeter.h`:

```c
void sayHello();
```

And well, the body of the library will of course live in a `greeter.c` file:

```c
#include <stdio.h>

void sayHello() {
    printf("Hello world\n");
}
```

Now it is just matter to tell to our CMake that we want to _build a library as well_:

```cmake
cmake_minimum_required (VERSION 3.6)
project (HelloCMake)
add_executable (hello hello.c)
add_library (libgreeter greet.c)
```

Run CMake again and done, you have your library... But wait, if you check the output you will see a static library, not a dynamic library!. This is because CMake, by default when building libraries will create a static library. Time to change that:


```cmake
cmake_minimum_required (VERSION 3.6)
project (HelloCMake)
add_executable (hello hello.c)
add_library (libgreeter SHARED greet.c)
```

Easy, now you will see your [dynamic library](https://en.wikipedia.org/wiki/Library_(computing)#Shared_libraries) there (.dynlib, .so, .dll) but sadly you are not doing anything with it. Time to change our `hello.c` file a little:

```cmake
#include "greeter.h"

int main() {
    sayHello();
}
```

Now, if we try to compile this it will fail! well, this happens because we are building the library but _not linking to it_. Let's fix that in the CMakeLists.txt file:

```cmake
cmake_minimum_required (VERSION 3.6)
project (HelloCMake)
add_executable (hello hello.c)
add_library (libgreeter SHARED greet.c)
target_link_libraries (hello libgreeter)
```

You can see the pattern here, when using CMake functions put first the destination and later the sources.

Well, I think it is enough for today with simple CMake files, we will continue later with more about CMake.
