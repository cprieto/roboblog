---
title: CMake and Threads
date: 2021-03-05
slug: cmake-and-threads
tags: c++, native, cmake, programming
---

For a while a book that had been in my shelf, asking to be read, has been [C++ Concurrency in Action, Second Edition](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition) by Anthony Williams and published by [Manning](https://www.manning.com/). Long story short, it is an amazing book, if you are new to concurrency or want to learn more about it (it doesn't matter you are not into C++), give it a read!.

Anyway, I was writing the examples in C++ and I noticed something interesting with [CMake](https://cmake.org/), let me explain with a toy example:

```cpp
#include <iostream>
#include <thread>

int main() {
    std::thread t([] {
        std::cout << "hello concurrent world!\n";
    });
    t.join();
}
```
As you see, something simple, we use the `thread` header in the standard library introduced in the C++11 standard, let's build a simple `CMakeLists.txt` to build with CMake using C++17:

```cmake
cmake_minimum_required(VERSION 3.15)
project(hello)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(hello main.cpp)
```

As usual, we build with the typical `cmake` and `cmake --build .` as usual (remember to do this in an out-of-source directory!) and guess what, it builds without any problems! (in Windows and macOS).

But if you try to build the same sample in Linux we have a surprise!

```
main.cpp:(.text+0xd9): undefined reference to `pthread_create'
```

Wow, an error! it cannot find the `pthread` library when linking. I was actually expecting something like that but it didn't fail at all in macOS and Windows, why? because in macOS and Windows you don't require an external library for threading (so it is included already) while in Linux (and probably FreeBSD) you will need to specify a threading library to use. Knowing this we change the CMakeLists.txt file to this:

```cmake
cmake_minimum_required(VERSION 3.15)
project(hello)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Threads REQUIRED)

add_executable(hello main.cpp)
target_link_libraries(hello Threads::Threads)
```

Done, if we try to compile in Linux it will just work! in macOS it will pass the `-pthread` parameter to LLVM and it will be ignored while in Windows it will just tell you `pthreads.h` is not found but CMake will find a Threads library anyway, compiling without problems!
