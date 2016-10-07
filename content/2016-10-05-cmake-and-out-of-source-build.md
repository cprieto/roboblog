---
title: CMake and out-of-source build
date: 2016-10-05
slug: cmake-out-of-source-build
tags: native, cmake, programming
---

Hello, it is me again! What were we talking about the last time? Oh yeah! CMake! Well, here I am, ready to talk more about CMake! Ready? Let's go!

So far we have been building our simple build script in the same directory as our source code. In the same directory as our `CMakeList.txt` file you will see:

 * Compiled executable files (if any)
 * Compiled library files (if any)
 * Generated Makefile (if that is your default)
 * `CMakeCache.txt` file: as the name says, a cache for CMake with variables and settings
 * `cmake_install.cmake` file, it has the instructions about how to _install_ your compiled application or library
 * `CMakeFiles` directory, with a bunch of temporary files used by CMake to do a bunch of things

As you may already see, there are a lot of things in the same directory as our source code which are mostly generated code and are not actually relevant to our application. It could be a great idea to put the compiled artefacts in a place, the generated files in another and the source code in another... It could be so clean!

So far what we have been doing is called **in-source building**; it is the default behaviour where the compiled artefacts as well as CMake generated files are located in the same directory. This is not the recommended way to use CMake, yes, it is the default because it is simple, but it should not be used _even in your examples_ (well, I used because I wanted to explain other things first!).

The alternative is called **out-of-source building** and there is not a way to do it from the CMakeLists.txt file! In fact, the recommended way is doing this in the command prompt (or console):

```
mkdir build
cd build
cmake ..
```

In other words, create the build directory, cd to that directory and then tell to CMake to generate the files from the CMakeLists.txt file in the root directory. If you do that right now with your current project you will see the build libraries and executables together with the generated CMake files are in the `build` directory. Believe it or not, this is the way CMake recommends to do the out-of-source builds: make the build directory, cd to that directory, run CMake against the parent directory.

There is no variable or global mechanism to do this from the CMakeLists.txt file, nope, nothing... but there is an _undocumented_ set of parameters for the CMake command line to do the same, again, this is **undocumented** and it could break any time soon; it currently works with my version of CMake (3.6) but who knows about tomorrow...

```
cmake -H. -Bbuild
```

The first parameter tells you where the CMakeLists.txt file is, and the second where the build artefacts directory is. Notice that `-H` is the _help_ parameter in the official CMake documentation and `-B` is not even documented. Again, this is an _undocumented_ feature and it could break any time soon; handle with care!

In both cases, to build from the new build artefacts directory you just use the build command of CMake:

```
cmake --build build --clean-first
```

In this case, we tell CMake where the CMakeCache file is and ask it to build. I passed the option to clean the artefacts first as well.

# Placing the artefacts

Right now the generated files created by CMake are in the same directory as the build executables and libraries; it is time to tell to CMake to place them in a separate directory. Let's do that by changing the CMakeLists.txt file and placing the compiled binaries in the `output` directory:

```cmake
cmake_minimum_required (VERSION 3.5)
project (HelloCMake)

set (PROJECT_SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)
set (HELLO_SOURCES ${PROJECT_SOURCE_DIR}/hello.c)
set (LIBHELLO_SOURCES ${PROJECT_SOURCE_DIR}/libhello.c)

# These are the corresponding output paths
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)
set (LIBRARY_OUTPUT_PATH ${EXECUTABLE_OUTPUT_PATH})

add_executable (hello ${HELLO_SOURCES})
add_library (libhello SHARED ${LIBHELLO_SOURCES})
```

As you can see, we produce a shared library and an executable; both of them are placed in the `output` directory. We do this just by changing the content of the variables `EXECUTABLE_OUTPUT_PATH` and `LIBRARY_OUTPUT_PATH`.

If we run our CMake build again, we will have now an output directory with both files, the executable and DLL (or SO or dSYM)... easy!

I think that was enough CMake for today... I will come back later with something else or who knows, more CMake, we still have a long road to explore!
