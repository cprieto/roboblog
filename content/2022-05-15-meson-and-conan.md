---
title: Meson and Conan
date: 2022-05-15
slug: meson-and-conan
tags: meson, native, programming, building, conan
twitter_image: meson_lego_man.png
---
Ok, I had talked a lot about [Conan](https://conan.io/) in the past and how it integrates nicely with build systems like [CMake]({filename}/2021-03-14-simpler-cmake-with-conan.md). Conan has a really huge list of packages and is really simple to use but sadly, there are no straigh instructions about using Meson with Conan... Imagine that, your build in Meson but you need some dependencies that are not Meson subprojects, you just find the required package, download it using Conan and voila! life is nice again.

Let's take a simple example, [fmt](https://github.com/fmtlib/fmt) is a simple formatting library, it uses CMake as build system and there is no wrapdb package for it.

```cpp
#include <fmt/core.h>

int main() {
    fmt::print("Hello world!\n");
}
```

Of course it won't work, we don't have `fmt` installed as a dependency, let's solve that with a `conanfile.txt`:

```ini
[requires]
fmt/

[generators]
cmake_find_package
```

Notice the `cmake_find_package` generator, it is important, you will get why soon. Now it is time for our first attempt for the build file:

```meson
project('meson_conan', 'cpp', default_options: ['cpp_std=c++17'])

fmt = dependency('fmt')
executable('demo', 'main.cpp', dependencies: [fmt])
```

Nothing new there, we just tell it to find the `fmt` dependency and compile our executable, but of course if we try to build this it will tell us it cannot find the dependency `fmt`, no worries, that is expected, the dependency is not _installed_ yet and needs to be manually set first. We can do that automatically using the `run_command` in our Meson build file:

```meson
project('meson_conan', 'cpp', default_options: ['cpp_std=c++17'])

run_command('conan', 'install', '--install-folder', 
    meson.build_root(), meson.source_root(), 
    '--build=missing')

fmt = dependency('fmt')
executable('demo', 'main.cpp', dependencies: [fmt])
```

With this, during _setup_, Meson will run Conan, it will install `fmt` _before_ checking the dependency (we could probably create a "dependency" between the _dependency_ and the command, but I have no idea how to do that yet!) and guess what, it still does not work!

The reason is how the Meson build system checks for dependencies, you can see the details [here](https://mesonbuild.com/Dependencies.html#dependency-detection-method), because we are generating CMake's find package files this should work, but the problem is that Meson does not know where to find such files, we need to give it a "hint":

```meson
project('meson_conan', 'cpp', default_options: ['cpp_std=c++17'])

run_command('conan', 'install', '--install-folder', 
    meson.build_root(), meson.source_root(), 
    '--build=missing')

fmt = dependency('fmt', cmake_module_path: meson.build_root())
executable('demo', 'main.cpp', dependencies: [fmt])
```

Of course you need CMake installed for this to work! and now if you try, voila! it finds the dependency and compiles nicely! :D
