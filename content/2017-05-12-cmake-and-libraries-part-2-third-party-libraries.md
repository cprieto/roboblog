---
title: CMake and Libraries, part 2, third party libraries
date: 2017-05-12
slug: cmake-and-libraries-part-2-third-party-libraries
tags: native, cmake, programming, make, makefile, c, gtk3
---

Last time we dealt with adding _subprojects_ to a main CMake project, this is very typical because, you know, sometimes C/C++ projects are _really big_. Another very common thing in big projects is using third party libraries, yes, libraries that you know should be previously installed in your machine and your application depends on it, this is specially important in _Unix platforms_ where we don't have a unique ecosystem for things like globalisation and user interfaces (_do you prefer GTK or Qt?_).

Let's say you are developing an application to run in the [Gnome Desktop environment](https://www.gnome.org/), the _core_ of this desktop environment is a UI library known as [GTK](https://www.gtk.org/), and let's say you decided to learn GTK and start doing your projects using CMake... Well, let's do it.

For a simple example let's go to the [getting started with GTK3](https://developer.gnome.org/gtk3/stable/gtk-getting-started.html) page and put the `app.c` example in the `src` directory for our project:

```cpp
#include <gtk/gtk.h>

static void activate (GtkApplication* app, gpointer user_data) {
  GtkWidget *window = gtk_application_window_new (app);
  gtk_window_set_title (GTK_WINDOW (window), "Window");
  gtk_window_set_default_size (GTK_WINDOW (window), 200, 200);
  gtk_widget_show_all (window);
}

int main (int argc, char **argv) {
  GtkApplication *app = gtk_application_new ("org.gtk.example", G_APPLICATION_FLAGS_NONE);
  g_signal_connect (app, "activate", G_CALLBACK (activate), NULL);
  int status = g_application_run (G_APPLICATION (app), argc, argv);
  g_object_unref (app);

  return status;
}
```

The instructions for compiling this example are simple, in the source directory just tell to GCC how to compile the app (you will need the required build components of course):

```
gcc `pkg-config --cflags gtk+-3.0` -o example-0 example-0.c `pkg-config --libs gtk+-3.0`
```

The secret sauce here is the [pkg-config](https://en.wikipedia.org/wiki/Pkg-config) command, it tells the compiler important things to know when compiling, like _where are the include files for this specific library_ or _this library needs the following parameters_. That is basically what the `--cflags` part tells in the first command (the location of the header files and required flags) and the `--libs` just pass the parameters needed for linking the libraries. That is a classic example of building applications with third parties in Linux, no really, it is super common even for hello world!.

How do we do the same with CMake? Well, as usual there are many ways to peel this fruit. Let's start with the basic CMake skeleton for our project:

```cmake
cmake_minimum_required (VERSION 3.6)
project (hello_gtk)

set (SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)
set (HELLO_GTK_SOURCE ${SOURCE_DIR}/app.c)
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)

add_executable (app ${HELLO_GTK_SOURCE})
```

Of course this is not going to work as is, first we need to tell to CMake to use the _helper macros_ for PkgConfig using the _package_ for PkgConfig:

```cmake hl_lines="4 5"
cmake_minimum_required (VERSION 3.6)
project (hello_gtk)

find_package (PkgConfig REQUIRED)
pkg_check_modules (GTK3 REQUIRED gtk+-3.0)

set (SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)
set (HELLO_GTK_SOURCE ${SOURCE_DIR}/app.c)
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)

add_executable (app ${HELLO_GTK_SOURCE})
```

The package `PkgConfig` is included with CMake, then we use the macro `pkg_check_modules` to check for the `gtk+-3.0` library, this is the same name we will pass to the `pkg-config` command line.

We are not ready to build yet, we have to tell to CMake where are our include directories and our libraries. The `PkgConfig` package does this with the variables `INCLUDE_DIRS` and `LIBRARY_DIRS` with _the prefix we specified when calling pkg_check_modules_, in this case, `GTK3`. Now our `CMakeLists.txt` file will look like this:

```cmake hl_lines="11 12"
cmake_minimum_required (VERSION 3.6)
project (hello_gtk)

find_package (PkgConfig REQUIRED)
pkg_check_modules (GTK3 REQUIRED gtk+-3.0)

set (SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)
set (HELLO_GTK_SOURCE ${SOURCE_DIR}/app.c)
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)

include_directories (${GTK3_INCLUDE_DIRS})
link_directories (${GTK3_LIBRARY_DIRS})

add_executable (app ${HELLO_GTK_SOURCE})
```

Now it is easier, we only have to tell to CMake to link against our libraries, again the `PkgConfig` package creates the `LIBRARIES` variable with the specified prefix:

```cmake hl_lines="15"
cmake_minimum_required (VERSION 3.6)
project (hello_gtk)

find_package (PkgConfig REQUIRED)
pkg_check_modules (GTK3 REQUIRED gtk+-3.0)

set (SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)
set (HELLO_GTK_SOURCE ${SOURCE_DIR}/app.c)
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)

include_directories (${GTK3_INCLUDE_DIRS})
link_directories (${GTK3_LIBRARY_DIRS})

add_executable (app ${HELLO_GTK_SOURCE})
target_link_libraries (app ${GTK3_LIBRARIES})
```

One last thing, some libraries, like GTK3, needs additional flags when building, for example, `-pthread` to indicate reentrancy. This is not passed immediately to the compiler with our current configuration. To do this `PkgConfig` creates an additional variable named `CFLAGS_OTHER` and we can pass that to CMake with the macro `add_definitions`:

```cmake hl_lines="13"
cmake_minimum_required (VERSION 3.6)
project (hello_gtk)

find_package (PkgConfig REQUIRED)
pkg_check_modules (GTK3 REQUIRED gtk+-3.0)

set (SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)
set (HELLO_GTK_SOURCE ${SOURCE_DIR}/app.c)
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/output)

include_directories (${GTK3_INCLUDE_DIRS})
link_directories (${GTK3_LIBRARY_DIRS})
add_definitions (${GTK3_CFLAGS_OTHER})

add_executable (app ${HELLO_GTK_SOURCE})
target_link_libraries (app ${GTK3_LIBRARIES})
```

And that is all for today, you can see more information about the `PkgConfig` package in the [documentation](https://cmake.org/cmake/help/latest/module/FindPkgConfig.html). There are _multiple_ modules included with CMake to do and find many things and popular libraries (like [Google Test](https://cmake.org/cmake/help/latest/module/FindGTest.html)), there are many third party modules as well, maybe I will explain how to use those third parties modules in the next blog post ;)
