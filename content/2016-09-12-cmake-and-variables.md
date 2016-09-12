---
title: CMake and variables
slug: cmake-and-variables
date: 2016-09-10
tags: cmake, build, native, programming
---

Yeah, it is me again with more CMake!

You remember last blog post? when I told you it was the [simplest CMake build file possible](the-simplest-cmake-possible)? Well, I lied. In fact, if we just want to print _Hello world_ in CMake we just need to do something like this:

```cmake
# we just print hello world
message("Hello world!")
```

It does absolutely nothing, but just say Hello world when generating the Makefile, and of course, your Makefile will do absolutely nothing.

# Variables

So I have been talking only about CMake **Commands**, `add_executable`, `link_target_library` and `message` are _commands_ in CMake, they tell CMake what to do and CMake will know how to do it. CMake has a lot of commands and all of them are documented in the [CMake documentation](http://cmake.org/cmake/help/v3.6/manual/cmake-commands.7.html).

As every modern scripting "language", CMake has _variables_ too, and some of those variables are _special_ and provide special information from CMake, like the directory path where the sources are, the place where we put the compiled executables and libraries, etc. The same as commands, there are a lot of [useful variables](https://cmake.org/Wiki/CMake_Useful_Variables) listed in the CMake wiki and documentation.

## Setting variables

Set a variable in CMake is really easy, you just need the command `set`:

```cmake
cmake_minimum_required (VERSION 3.5)
project (CMakeVariables)
set (SOURCES hello.c greeter.c)
add_executable (hello ${SOURCES})
```

We just created _a list of files_ in our variable `SOURCES` and then use that variable in a target. Easy!

# Where are the header files?

Header files are important in C/C++ development and usually they live in a separate directory. Let's change that in our current project:

```bash
mkdir includes
mv greeter.h includes
```

Of course we will need to change our CMakeLists.txt file to reflect this change:

```cmake
cmake_minimum_required (VERSION 3.5)
project (CMakeVariables)
set (SOURCES hello.c greeter.c)
include_directories (${PROJECT_SOURCE_DIR}/includes)
add_executable (hello ${SOURCES})
```

As you can see, we need to use the `include_directories` command to tell CMake where to find our header files.

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
