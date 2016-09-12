---
title: CMake and variables
slug: cmake-and-variables
date: 2016-09-10
tags: cmake, build, native, programming
---

Yeah, it is me again, with more CMake!

You remember last blog post? when I told you that was the [simplest CMake build possible]()? well, I lied. In fact, if we just want to do the equivalent _Hello world_ in CMake something like this will be enough:

```cmake
# we just print hello world
message("Hello world!")
```

That does absolutely nothing, but just say Hello world when generating the Makefile, and of course, your Makefile will do absolutely nothing.

# CMake and variables

So far I had introduced to you only to CMake `Commands`, yes, `add_executable`, `link_target_library` and `message` are _commands_, they tell to CMake what to do and believe me, there are _plenty_ of commands to do a lot of things!.

Well, as every modern script "language", CMake has _variables_ too, and some of those variables are _special_ and provided with CMake to provide certain information, like the directory where the sources are, the place where we put the libraries and so on. The same as commands, there are a lot of [useful variables](https://cmake.org/Wiki/CMake_Useful_Variables) the same as a [lot of commands](https://cmake.org/cmake/help/v3.6/manual/cmake-commands.7.html) to do a bunch of things, for example, a very useful variable is `PROJECT_SOURCE_DIR` which points to the current directory where CMake expects the source code:

```cmake
message(${PROJECT_SOURCE_DIR})
```

As you can see, by default the source directory is the same path where we have the `CMakeLists.txt` file.

# Setting variables

Set a variable in CMake is really easy, we just use the command `set`:

```cmake
cmake_minimum_required (VERSION 3.5)
project (CMakeVariables)
set (SOURCES hello.c greeter.c)
add_executable (hello ${SOURCES})
```

Let's forget about our `greeter.h` file for a while. As you may expect it will compile, and you can see we can put _a list of files_ in our variables as well (in this case both files are listed as required for our executable). Variables in CMake are awesome and we will use them a lot in the future.

# Where are the header files?

As I mentioned before, we forgot about the header file (which are very important in C/C++ development), let's tell to CMake that our headers are in the same directory as the source:

```cmake
cmake_minimum_required (VERSION 3.5)
project (CMakeVariables)
set (SOURCES hello.c greeter.c)
include_directories (${PROJECT_SOURCE_DIR})
add_executable (hello ${SOURCES})
```

This is kind of equivalent to appending the directory to the variable `INCLUDE_DIRECTORIES` (see [the documentation](https://cmake.org/cmake/help/v3.6/command/include_directories.html)) but it looks nicer and give us more flexibility to use the command instead of setting the variable directly. By default this variable points as well to the same directory as `PROJECT_SOURCE_DIR` and that is the reason we didn't have problems before. It is good idea to set this on.

# File globbing

Instead of creating a variable with a explicit list of source files we can "glob" them together using an expression and assign the created list to a variable, this is done with the [`file`](https://cmake.org/cmake/help/v3.6/command/file.html?highlight=glob#file) command:

```cmake
cmake_minimum_required (VERSION 3.5)
project (CMakeVariables)
include_directories (${PROJECT_SOURCE_DIR})
file (GLOB SOURCES *.c)
add_executable (hello ${SOURCES})
```

**Note about globbing!** : Even the CMake documentation warns us about globbing and ask us to _explicitly list the source files_ instead of using globbing. This [question from StackOverflow](http://stackoverflow.com/questions/1027247/best-way-to-specify-sourcefiles-in-cmake) explains a little more about the issue and the options.

In conclusion, use globbing with caution!

Well, now we know about variables in CMake and file globbing, but we still have a few other things to explore in CMake, so I will see you soon with another short blog post!.
