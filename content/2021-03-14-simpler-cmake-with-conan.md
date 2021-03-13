---
title: CMake and Threads
date: 2021-03-14
slug: simpler-cmake-with-conan
tags: c++, native, cmake, programming
twitter_image: dependencies.jpg
---

I had already written about using [Conan and CMake]({filename}/2020-10-26-handling-external-dependencies-in-cplusplus-with-conan.md) to handle your C++ dependencies and that is a setup I had used for a while now. Recently, while working in a few things with the [Boost](https://www.boost.org/) library, I found the cracks in this setup, for example, this setup does not support handling components, something really useful when using Boost.

While asking around, I realised while this is the way most documentation is written, it is not the preferred way to use dependencies with Conan and CMake, it is not that we have to change much but the generator, instead of using the `cmake` generator, we should use the `cmake_find_package` generator. This generator will create files named `FindXXX.cmake` where `XXX` is the dependency we are included.

Let's use the example from the previous blog post, but instead changing the generator to use:

```ini
[requires]
nlohmann_json/3.9.1

[generators]
cmake_find_package
```

Now, we need to remove from CMake the previous setup and use, instead, the native `find_package` facility, now created thanks to Conan:

```cmake
cmake_minimum_required (VERSION 3.15)
project (sample)

find_package(nlohmann_json REQUIRED)

add_executable (main main.cpp)
target_link_libraries (main nlohmann_json::nlohmann_json)
```

Notice the usage of `nlohmann_json::nlohmann_json`  in the dependencies, this is the name and component of your dependency.

Let's try to install and compile this:

```
mkdir build && cd build
conan install ..
cmake ..
```

This will faill with a message about `Findnlohmann_json.cmake` not found in `CMAKE_MODULE_PATH`. That is weird, isn't it? I mean, if we check that file is in the build directory, what is happening? Well, it is exactly that, the file is in the build directory and not where your CMake expects the file to live, we can fix this easily _appending_ the file to our module path:

```cmake
cmake_minimum_required (VERSION 3.15)
project (sample)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
find_package(nlohmann_json REQUIRED)

add_executable (main main.cpp)
target_link_libraries (main nlohmann_json::nlohmann_json)
```
Try running the same commands again, voila! it works! now it is time to compile with the usual command:

```
cmake --build . --clean-first
```
