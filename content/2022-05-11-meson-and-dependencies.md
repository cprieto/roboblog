---
title: Meson and dependencies
date: 2022-05-11
slug: meson-and-dependencies
tags: c++, native, programming, meson, building
twitter_image: meson_dependencies.png
---

I know [Meson](https://mesonbuild.com/index.html) has been out for a while and somehow those days it didn't fit into my workflow. Times had changed and now is a pretty awesome build system, supported by a wide range of projects (especially in Linux) and many IDEs and editors (for example, [CLion](https://wanzenbug.xyz/clion-meson-compiledb/) and [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=mesonbuild.mesonbuild)). I don't even need to explain how to build with Meson, the documentation is _amazing_ and so easy to follow, you can be productive building your project in no time!

Your project rarely lives in isolation and depends on other libraries, installed or not in your machine, so how does Meson would fit in those scenarios? I did a few experiments and went through the documentation and decided to put what I learned about dependencies in a few posts, this is the first one of those.

## Meson and wraps

Meson has the concept of [subprojects](https://mesonbuild.com/Subprojects.html), that is, other projects you depend on can be placed with their own dependencies and builds in a separate project or place. With _external_ projects, you know, those living in GitHub or some other place, you have what Meson calls [wraps](https://mesonbuild.com/Wrap-dependency-system-manual.html) which basically is just a small file with metadata about how to grab your project and exported dependencies. Meson offers a database of existing _wraps_ (known as [wrapdb](https://mesonbuild.com/Using-the-WrapDB.html)) and tooling to easy the process.

Let's take a simple example from [handling dependencies with Conan]({filename}/2020-10-26-handling-external-dependencies-in-cplusplus-with-conan.md) blog post:

```cpp
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
        auto entry = json::parse(R"({ "name": "cristian" })");
        std::cout << "His name is: " << entry["name"] << "\n";
}
```

We need the excelent [nlohmann JSON library](https://github.com/nlohmann/json), and affortunately they are listed in the WrapDB (the library actually offers a CMakeLists and Meson build files), so to include this as a wrap dependency we just type in the command line (you need to have the `subprojects` directory created):

```
meson wrap install nlohmann_json
```

This will install a very small `.wrap` file telling us things like where to get the source code and, more importantly, what is the name of the exported dependencies, in this case `nlohmann_json`:

```
[wrap-file]
directory = nlohmann_json-3.10.5
lead_directory_missing = true
source_url = https://github.com/nlohmann/json/releases/download/v3.10.5/include.zip
source_filename = nlohmann_json-3.10.5.zip
source_hash = b94997df68856753b72f0d7a3703b7d484d4745c567f3584ef97c96c25a5798e

[provide]
nlohmann_json = nlohmann_json_dep
```

In our `meson.build` file we just add this as a dependency, as any other dependency (as described in the [dependency](https://mesonbuild.com/Dependencies.html) segment in the documentation):

```meson
project('demo', 'cpp', version: '1.0')

nlohman_json = dependency('nlohmann_json')

executable('demo', 'main.cpp', dependencies: [nlohman_json])
```

Done! this will build nicely in Windows and Linux!. In macOS you will probably have some weird syntax errors, this is mostly because you need C++11 or higher to use this JSON library, that is no problem, just set the required parameters in your Meson file if we are running in macOS:

```meson
project('hello_cristian', 'cpp', version: '1.0')

if build_machine.system() == 'darwin'
    add_project_arguments('-std=c++17', language : 'cpp')
endif

nlohman_json = dependency('nlohmann_json')

executable('demo', 'main.cpp', dependencies: [nlohman_json])
```

You can get as creative as you want with the `if` statement, but just with that simple example you see how nice our build file looks like!