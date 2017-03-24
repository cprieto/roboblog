---
title: CMake and Libraries, part 1
date: 2017-03-24
slug: cmake-and-libraries-part-1
tags: native, cmake, programming, make, makefile, c
---

I must tell you the truth, not all applications out there are as simple as a _hello world_, yes, I know, shocking right?! and so far we have been doing simple CMake files to produce a simple application with a few files. Today let's try to cover a little more complicated scenario with application depending and producing libraries, it will be fun!

# The project

Let's start with our project structure:
```
.
├── CMakeLists.txt
├── hello_app
│   ├── CMakeLists.txt
│   └── src
├── libgreeter
│   ├── CMakeLists.txt
│   ├── includes
│   └── src
└── output
```
We will put our library `libgreeter` (the greatest hello library out there!), its source in the `src` directory and its _header_ files in the `includes` directory. Our executable application will live in the `hello_app` directory and its source in the `src` folder, hello_app depends on libgreeter (it will be statically linked) and we will compile a static and shared library for libgreeter. Finally, we will place the output of everything in the `output` directory and [_out of source build_]({filename}2016-10-05-cmake-and-out-of-source-build.md) in the `build` folder. Notice we have a *root* `CMakeLists.txt` file and a corresponding file for the library and the "main" program. This is to make our build process much more modular and maintainable, yes, we can make all the build with just _one_ CMake list file but I _won't recommend_ that (me and almost everybody else in the internet).

The code for `greeter.h` header library in the `libgreeter/includes` directory is pretty simple:

```c
#ifndef GREETER_H
#define GREETER_H

void say_hello_to (char *name);

#endif
```

Its implementation lives in `libgreeter/src/greeter.c`:

```c
#include <stdio.h>
#include "greeter.h"

void say_hello_to (char *name) {
    printf("hello %s\n", name);
}

```

Can we put the header and the source in the same directory for the greeter library? Yes! you can! but because we are expecting our amazing library to be used by other programs or libraries we decide to make those header public and place them apart. This is a very common layout for libraries and projects in CMake.

The `CMakeLists.txt` file for our greeter library (not the root list file) is the typical library list file:

```cmake
cmake_minimum_required (VERSION 3.6)
project (libgreeter VERSION 1.0)

include_directories (${CMAKE_CURRENT_SOURCE_DIR}/includes)

set (GREETER_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
set (GREETER_SOURCE ${GREETER_SOURCE_DIR}/greeter.c)

add_library (greeter SHARED ${GREETER_SOURCE})
add_library (greeter_static STATIC ${GREETER_SOURCE})
```

Notice the usage of `CMAKE_CURRENT_SOURCE_DIR` to point to the _current directory this CMakeLists.txt file is located_, if we don't do that it will point to the directory of the root project.

Let's move to the _root_ `CMakeLists.txt`, it is a little different of what we had written so far:

```cmake
cmake_minimum_required (VERSION 3.6)
project (hello VERSION 1.0)

set (LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)

add_subdirectory (libgreeter)
```

The `add_subdirectory` line tells CMake to include that directory project as part of the build, like a cascade project. I like that.

We are nearly done, let's test if we are building the library at least. In the root project directory do the classic out of source build:

```bash
mkdir build; cd build
cmake ..
cmake --build . --clean-first
```

Done, you should see a dynamic and static library binary in the `output` directory.

# The application

Now it is time to move to our _main_ application, this is how our simple `hello_app/src/main.c` looks like:

```c
#include "greeter.h"

int main() {
    say_hello_to ("cristian");
}
```

Now it is time to define `hello_app/CMakeLists.txt` file:

```cmake
cmake_minimum_required (VERSION 3.6)
project (hello_app VERSION 1.0)

set (HELLO_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
set (HELLO_SOURCES ${HELLO_SOURCE_DIR}/main.c)

add_executable (hello_app ${HELLO_SOURCES})
target_link_libraries (hello_app greeter)
```

Let's change the _root_ `CMakeLists.txt` file, now it will look like this:

```cmake
cmake_minimum_required (VERSION 3.6)
project (hello VERSION 1.0)

set (LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)

add_subdirectory (greeter)
add_subdirectory (hello_app)
```

If you try to run this as is **it won't work**. We are including `greeter.h` but that file it is not in our source tree, we could probably add an `include_directories` pointing to the directory where the `greeter.h` is located but that will be a killer in our pursuit of modularization. The secret is adding _one line_ to our `libgreeter/CMakeLists.txt` file, it should now look like this:

```cmake
cmake_minimum_required (VERSION 3.6)
project (libgreeter VERSION 1.0)

include_directories (${CMAKE_CURRENT_SOURCE_DIR}/includes)

set (GREETER_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
set (GREETER_SOURCE ${GREETER_SOURCE_DIR}/greeter.c)

add_library (greeter SHARED ${GREETER_SOURCE})
add_library (greeter_static STATIC ${GREETER_SOURCE})

target_include_directories (greeter PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/includes)
```

See the last line? it basically tells to CMake "hey, this directory I am putting here is a public include headers directory, pass that info to everybody else in the project".

Now try to build the whole project again... You will see the executable `hello_app`, a static library and a dynamic library for the greeter project as well.

# Next

What if the library is not made in CMake? what if the library is a third party library already in the system? what if not?... Well, I will try those ideas later in another blog post(s), wish me luck!

As usual, you can find the source code for this in a [GitHub Gist](https://gist.github.com/cprieto/79f3c5c7907dcc64dfca949e06b3c970)
