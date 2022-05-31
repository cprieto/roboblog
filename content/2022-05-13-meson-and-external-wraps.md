---
title: Meson and external wraps
date: 2022-05-13
slug: meson-and-external-wraps
tags: meson, native, programming, building
twitter_image: meson_wraps.png
---

Ok, [last time]({filename}/2022-05-11-meson-and-dependencies.md) I mentioned how to include wraps from the wrapdb into a meson build and it was all happy! But what if the dependency we need is **not** in the wrap database?

Well, as many other things in engineering, _it depends_, the most simplest case (what I am going to document today) is when the dependency is "somewhere" and is using Meson too. Let's take a simple case, there is a test library for C, [Criterion](https://github.com/Snaipe/Criterion), in the repository we can see they are using Meson (see that `meson.build` file?) so is perfect for our case!

Let's start with our simple test project:

```c
#include <criterion/criterion.h>

Test(simple, test) {
    cr_assert(0, "Hello world");
}
```

Ok, time for the simplest build file (ignore the `default_options` part, that is just to make `clang` happy in macOS):

```meson
project('test_criterion', 'c', default_options: ['cpp_std=c++17'])
criterion = dependency('criterion')
executable('test_criterion', 'test.c', dependencies: [criterion])
```

Ok, we will create our own wrap file to define Criterion as a dependency, we will grab the version 2.4.1 from the repository using Git, use a recursive cloning (Criterion uses Git submodules) with a simple depth of 1 (we don't need the whole history).

```
[wrap-git]
url = https://github.com/Snaipe/Criterion.git
revision = v2.4.1
depth = 1
clone-recursive = true

[provide]
criterion = criterion
```

Where that last part comes from? well, if we look at the file `src/meson.build` we will see this fragment:

```meson
criterion = declare_dependency(
	include_directories: [criterion_api],
	dependencies: deps,
	link_with: [libcriterion])
```

Telling us this build exports a dependency named `criterion`, we just say this library provides a dependency named criterion and we will use it under the name criterion (`my_dep = proj_dep`).

Done! on `meson build` it will grab Criterion and all its dependencies (including any wraps defined by Criterion) and with `meson compile -C build` we should see our `test_criterion` executable.