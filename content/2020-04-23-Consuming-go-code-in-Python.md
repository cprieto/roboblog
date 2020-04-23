title: Consuming Go code in Python
date: 2020-04-23
slug: consuming-go-code-in-python
tags: programming, python, go
twitter_image: books.jpg
---
We love [Python](https://www.python.org/), it is an amazing language for _almost_ everything out there. One of the problems that I always heard from people out there is _but Python is dynamic and that makes it slow_ and, well, that statement is usually _half true_. The performance implications of code in Python is not something I want to cover in this blog post, but instead how to use Python with something completely different, like [Go](https://golang.org/). If you are reading this blog post you probably already know what is Go and Python but just in case, Go is a very popular open source static language created by Google to replace the aging C language. It is _sometimes_ faster than Python and it is very common in certain companies to have a mix between Python and Go language (or any other static language).

Let's say you already have a super fancy algorithm written in Go but you need to consume that in a Python script. What I had seen so far is people rewriting the whole algorithm to Python to make it work and usually it results in a not very optimal algorithm (it is slow). What if we can just use the code in Go inside Python?. The simple example you will see out there is the simple formula to sum a sequence by [Gauss](https://hsm.stackexchange.com/questions/384/did-gauss-find-the-formula-for-123-ldotsn-2n-1n-in-elementary-school):

```go
func GSum(n int) (result int) {
    for i := 0; i <= n; i++ {
        result += i
    }
    return
}
```

Before consuming this in Python, we need to produce an object suitable for binary distribution, in the case of MacOS and Linux this is a [shared object](https://en.wikipedia.org/wiki/Library_(computing)) while in Windows this is a [dynamic loading library](https://en.wikipedia.org/wiki/Library_(computing)#Microsoft_Windows). The Go compiler can produce such thing, well, not directly the Go compiler but a helper, [CGo](https://golang.org/cmd/cgo/). The CGo compiler cannot generate the shared library by itself but it needs a C/C++ compiler and currently (as Go 1.14) the only supported compiler is [GCC](https://gcc.gnu.org/) so you need to install it if you don't have it already.

We need to do a few small changes to our function as well:

 - Your function needs to be in the `main` package
 - Your function needs to have a `main` function, even if that one is empty
 - Your function needs to import the "C" Go library
 - You need to mark your function as `export`

Let's say our function is saved in the file `sum.go`, the content of the file would look like this:

```go
package main

import "C"

//export GSum
func GSum(n int) (result int) {
    for i := 0; i <= n; i++ {
        result += i
    }
    return
}

func main() {
}
```

To compile this (in Windows) you only issue the following command:

```bash
go -buildmode=c-shared -o sum.dll sum.go
```

In Linux change `sum.dll` to `sum.so` and in MacOS change it to `sum.dynlib` (**Update**: the difference between _shared libraries_ and _dynamically loaded modules_ is kind of subtle and complex in reality, as pointed out in this [StackOverflow post](https://stackoverflow.com/questions/2339679/what-are-the-differences-between-so-and-dylib-on-osx) and this [GitHub issue](https://github.com/golang/go/issues/12700)).

Now it is time to consume it in Python, we use the included stadard library `ctypes` and `cdll` to first load the library and then consume it as any other Python function:

```python
from ctypes import cdll
gosum = cdll.LoadLibrary('./sum.dll') # or sum.so depending on your OS
print(gosum.GSum(100)) # It will print 5050
```

But is this faster in Go than in Python? well, let's implement the same in a more Pythonic way:

```python
def GSum(n: int) -> int:
    return sum(range(1, n + 1))
```

And when running some benchmarks (using PyTest and Benchmark) we get surprising numbers:

| Implementation | Min    | Max     | Median |
|----------------|--------|---------|--------|
| Python         | 1.0200 | 16.9200 | 1.0552 |
| Go lib         | 2.000  | 36.300  | 2.2095 |

As you may see, using the Go implementation (as a dynamic link library) is a lot slower than using the pure Python code. This **is not** because Python is faster than Go but because the problem we are trying to solve makes no sense to do it in Go in that way. Every time we call the external function in Python we use resources to consume the dynamic object and that affects the performance.

To see if that was the case I decided to write the same function in plain C and export it as a DLL in Windows:

```c
__declspec(dllexport) int gsum(int n) {
  int result = 0;
  for(int i = 0; i <= n; i++) {
    result += i;
  }
  return result;
}
```

The process to load it in Python is exactly the same (it is a DLL after all). To my surprise, this version was very fast:

| Implementation | Min  | Max   | Median    |
|----------------|------|-------|-----------|
| Python         | 1000 | 16580 | 1067.1030 |
| Go lib         | 2100 | 59900 | 2335.6452 |
| C lib          | 580  | 9660  | 595.2079  |

Contrary to what most people probably think, while Go creates a binary executable file, it runs inside a runtime with a garbage collector, so I think this is something that is slowing down the implementation. 

**Lesson learned**: Think twice before using dynamic load libraries from languages like Go in Python if your purpose is to gain speed in the execution of your algorithm, do your benchmarks _before_ writing your conclusions in stone.

There are more about interoperability between Python and dynamic load libraries in other languages, a topic that I will be probably exploring in a next blog post.

**NOTE**: Just for completeness this is my benchmark tests (`benchmark_gsum.py`) in Python. To use it remember to install [`pytest`](https://docs.pytest.org/en/latest/) and [`pytest-benchmark`](https://github.com/ionelmc/pytest-benchmark):

```python
from ctypes import cdll

gosum = cdll.LoadLibrary('./sum.dll')
cgsum = cdll.LoadLibrary('./cgsum/Debug/cgsum.dll')


def GSum(n: int):
    return sum(range(1, n+1))

def test_python_gsum(benchmark):
    assert benchmark(GSum, 100) == 5050

def test_go_gsum(benchmark):
    assert benchmark(gosum.GSum, 100) == 5050

def test_c_gsum(benchmark):
    assert benchmark(cgsum.gsum, 100) == 5050
```
