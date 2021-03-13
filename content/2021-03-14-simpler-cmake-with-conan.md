---
title: CMake and Threads
date: 2021-03-14
slug: simpler-cmake-with-conan
tags: c++, native, cmake, programming
twitter_image: threads.jpg
status: draft
---

I really love the mix between CMake and Conan to handle my C++ builds with dependencies and I had talked in the past about it, but what if I tell you, there is a better version to handle our dependencies and CMake with Conan? Well, strap in!

Let's start with the previous example:

```cpp
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
        auto entry = json::parse("{ \"name\": \"cristian\" }");
        std::cout << "His name is: " << entry["name"] << "\n";
}
```

And well, our `conanfile.txt` is simple enough, using [nlohmann json]() as a dependencies:

```ini
[requirements]
nlohmann_json/3.9.1

[generators]
cmake
```

And well, an even simpler `CMakeLists.txt` :

```cmake
cmake_minimum_required (VERSION 3.10)
project (sample)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable (main main.cpp)
target_link_library (main ${CONAN_LIBS})
```

There are many problems with this installation, it depends a lot of you knowing what to link and calling `conan_basic_setup`. 

# Find packages

Someone helped me to _improve_ my CMake with Conan, and instead of using the `cmake` generator, using another generator: `cmake_find_package` allows us to use the `find_package` command in CMake to find the dependencies directly (and this is very useful, because most of the documentation you read out there is using `find_package`), this generator will create files named `FindXXX.cmake` where `XXX` is the name of the dependency. Our file will look like this:

```cmake
cmake_minimum_required (VERSION 3.10)
project (sample)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
find_package(nlohmann_json REQUIRED)

add_executable (main main.cpp)
target_link_library (main nlohmann_json::nlohmann_json)
```

Why the `${CMAKE_BINARY_DIR}`? well, the problem is that CMake cannot find the generated `FindXXX.cmake` so we have to tell it to find it in the same file where is generated.

# Using 
