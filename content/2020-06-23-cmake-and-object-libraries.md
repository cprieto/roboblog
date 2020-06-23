title: CMake and object libraries
date: 2020-06-23
slug: cmake-and-object-libraries
tags: cmake, c++, build
twitter_image: library.jpg
---

I recently discovered [CMake](https://cmake.org) support for [Object Libraries](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html#object-libraries), those are, in simple words, not "_real_" libraries generating a `.lib`, `.so` or `.dll` files but _temporary_ libraries based in [Object files](https://en.wikipedia.org/wiki/Object_file). I find this very useful for supporting different build targets that depends in common code but I don't need to generate a _library_ at all.

Object libraries can easily be created like any other library using the `add_library` parameter, but passing the `OBJECT` option:

```cmake
add_library(sample OBJECT sample.cpp)
```

And later, we can link to this library as any other library but using `$<TARGET_OBJECT>` instead of the plain name of the library, for example:

```cmake
target_library(app $<TARGET_OBJECT:sample>)
```

Let's do a full example, our library header, `sample.h`:

```c++
class Sample {
public:
    int foo() const;
};
```

And now our implementation, `sample.cpp`:

```c++
#include "sample.h"

int Sample::foo() const { return 42; }
```

And of course, our user for the "library", `main.cpp`:

```c++
#include <iostream>
#include "sample.h"

int main() {
    Sample a{};
    std::cout << a.foo();
}
```

As you see, nothing fancy, but let's say that instead of listing `sample.cpp` as source for `app` you want to _link_ to it as a library, but creating a library for such a simple trivial piece of code sounds overkill, that is where the object library sounds super useful!

In your `CMakeLists.txt` file it will look something like this:

```cmake
cmake_minimum_required(3.1)
project(sample_obj LANGUAGES CXX)

add_library(sample OBJECT sample.cpp)
add_executable(app main.cpp)
target_link_libraries(app $<TARGET_OBJECTS:sample>)
```

And that is all, you can refer to `sample` as any other library as far as you use the expression `$<TARGET_OBJECTS:sample>` instead of the name of the library as you would do with a normal library.

## Some generators are nicer than others

The previous approach works very well with generators like `Visual Studio` or `Ninja` but as soon as you use `Makefiles` it will fail with a very cryptic error message:

```
make[2]: *** No rule to make target 'CMakeFiles/sample/sample.cpp.o', needed by 'app'.  Stop.
```

I was extremely surprised by this, I mean, it works _perfectly_ with any other generator but not with [Makefiles](https://en.wikipedia.org/wiki/Makefile), in fact, if you simply use something like [Ninja](https://ninja-build.org/) instead of Makefiles it will work without any problems at all. There is no mention of this in the documentation at all, in fact, the idea that it works in some generators and not in others really gives me no clue of what is the problem.

By pure trial and error I found a way to make this setup works (at least) with Makefiles, Ninja and Visual Studio, replacing `target_link_libraries` with `target_sources`:

```cmake
target_sources(app $<TARGET_OBJECTS:sample>)
```

I was still confused, why was it not working?

## Sometimes, not getting an error is actually the error

Having a chat with the CMake community I found my mistake, `$<TARGET_OBJECTS>` was never designed to be used with `target_link_libraries` in that way. Checking the documentation carefully it is very clear:

> The `OBJECT` library type defines a non-archival collection of object files resulting from compiling the given source files.  *The object files collection may be used as source inputs to other targets*:

And that is why it works using `target_sources`, the idea was never linking it directly as I was using it but use it in the same way you will declare sources, in my previous case would be enough to say:

```cmake
add_executable(app main.cpp $<TARGET_OBJECTS:sample>)
```

But since CMake 3.12 we can refer to object libraries directly as part of `target_link_libraries` without using the generator expression, in our previous case, our `CMakeLists.txt` will look like this:

```cmake
cmake_minimum_required(3.12)
project(sample_obj LANGUAGES CXX)

add_library(sample OBJECT sample.cpp)
add_executable(app main.cpp)
target_link_libraries(app sample)
```

Lesson learnt, when things are not working read the documentation again and again, until you understand what is happening.
