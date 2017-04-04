---
title: CMake and Libraries, part 1.5, Windows
date: 2017-04-02
slug: cmake-and-libraries-part-1.5-windows
tags: native, cmake, programming, make, makefile, c, windows
---

[Last time]({filename}2017-03-24-libraries-and-cmake-part-1.md) we built a CMake multidirectory C project and generated an executable as well as a static and a dynamic library. If you were running the code in macOS or Linux (or well, any Unix), you will see the `.dylib` file with the dynamic library (`.so` in Linux/FeeBSD) and `.a` file with the static library. If you try to run CMake in a Windows machine with the Visual C++ compiler chain installed you will see instead an error message telling you something like this:

!!! error ""
    LINK : fatal error LNK1104: cannot open file '..\..\output\Debug\greeter.lib' [C:\src\cmake_lib\build\hello_app\hello_app.vcxproj]

This is because in Windows a LIB file can be a [_static library_](https://msdn.microsoft.com/en-us/library/ms235627.aspx) and/or [_an import library_](https://msdn.microsoft.com/en-us/library/windows/desktop/ms682592(v=vs.85).aspx) which contains stubs to tell to the linker _how to link_ to the generated dynamic library. CMake gets confused and has no idea what file to use or generate for the static library, so we have to help it out and tell it the _same lib_ needs to be generated for both files.

Let's modify our `CMakeLists.txt` file for the library (inside the `libgreeter` directory) to add a conditional compilation statement. Notice the extra lines telling it to generate a `.lib` file with the same name for the greeter library:

```cmake hl_lines="12 13 14 15"
cmake_minimum_required (VERSION 3.6)
project (libgreeter VERSION 1.0)

include_directories (${CMAKE_CURRENT_SOURCE_DIR}/includes)

set (GREETER_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
set (GREETER_SOURCE ${GREETER_SOURCE_DIR}/greeter.c)

add_library (greeter SHARED ${GREETER_SOURCE})
add_library (greeter_static STATIC ${GREETER_SOURCE})

if (WIN32)
set_target_properties (greeter_static PROPERTIES OUTPUT_NAME Greeter CLEAN_DIRECTORY_OUTPUT 1)
set_target_properties (greeter PROPERTIES OUTPUT_NAME Greeter CLEAN_DIRECTORY_OUTPUT 1)
endif()

target_include_directories (greeter PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/includes)
```

Done, now if we try to compile this on Windows it will work as expected! NICE!
