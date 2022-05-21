---
title: Meson and threads
date: 2022-05-22
slug: meson-and-theads
tags: meson, native, programming, building, conan
---

Some time ago I wrote a small piece about [using the `Thread` dependencies in CMake]({filename}/2021-03-05-cmake-and-threads.md) and if I remember correctly it was a little tricky to set the correct threads library (Unix systems has a [pthreads library](https://en.wikipedia.org/wiki/Pthreads), for example). Guess what? is super easy to do it in Meson!

Let's see the example from that post:

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

The Meson build file couldn't be simpler:

```meson
project('meson_conan', 'cpp', default_options: ['cpp_std=c++17'])

threads = dependency('threads')

executable('demo', 'main.cpp', dependencies: [threads])
```

Notice the dependency name _should be_ `threads`, Meson will know the correct library to pick dependending on the operating system, nothing to worry about!
