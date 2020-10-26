---
title: Handling external dependencies in C/C++ with Conan
date: 2020-10-26
tags: c++, c, build, cmake, native, programming
slug: handling-external-dependencies-in-cplusplus-with-conan
---

Last time we saw how to handle [dependencies with vcpkg]({filename}/2020-10-12-handling-external-dependencies-in-cplusplus-with-vcpkg.md), an open source, cross platform package made by Microsoft trying to solve the external dependencies problem with native code. Vcpkg solves the problem in a centralized way, if you don't see a package you want to use, you ask in the issue tracker or make a PR with a patch, cmake file and required files to make the package work in the application build. Everything is in the same directory and repository (see the `/ports` directory) and that is why you need to update your repository and vcpkg application once in a while if you want updates.

[Conan](https://conan.io) is another popular cross platform package manager for C/C++, its approach is slightly different. In Conan, the developer has complete control of the package creation and build packages are available (so you don't have to build the package from scratch just to use it). Maybe the best way to explain the difference is doing the same example as last time but now with Conan.

First, let's install Conan, it is a Python application so you need Python installed in your machine. The [instructions]() in the official page are clear but in my case, I installed it using [Homebrew](https://brew.sh/) in my macOS and [Scoop](https://scoop.sh/) in Windows and the `pip` method in Linux. Just follow the instructions, it is that easy.

