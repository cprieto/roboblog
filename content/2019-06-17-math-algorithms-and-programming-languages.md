---
title: Math, algorithms and programming languages
date: 2019-06-17
slug: math-algorithm-and-programming-languages
tags: programming, math, ocaml, python, elixir
---

A few weeks ago I started reading [Number Theory for Computing](https://www.amazon.com/Number-Theory-Computing-Song-Yan/dp/3540430725) by Song Y. Yan (amazing book by the way!) and in the first chapter we learned about the [Euclidean Algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm), or how to find the Greatest Common Divisor, probably the oldest non trivial algorithm surviving to the present days (which, btw, probably wasn't "invented" by Euclid but "documented"). 

What called my attention is the way we take the algorithm and model or move it into a programming language, a quick search got me this answer from [StackOverflow](https://stackoverflow.com/questions/11175131/code-for-greatest-common-divisor-in-python), I will copy the second answer from that question:

```python
def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x
```

This is very similar to the "loop" code in the previous Wikipedia article:

```algo
function gcd(a, b)
    while b ≠ 0
       t := b; 
       b := a mod b; 
       a := t; 
    return a;
```

Wikipedia has a recursive version as well:

```algo
function gcd(a, b)
    if b = 0
       return a; 
    else
       return gcd(b, a mod b);
```

And the same StackOverflow question has a recursive answer too:

```python
def gcd_recursive(a, b):
    if b == 0:
        return a
    else:
        return gcd_recursive(b, a % b)
```

I decided to implement the same algorithm using Elixir first to see how "clear" would it look:

```elixir
defmodule Num do
  def gcd(a, 0), do: a
  def gcd(a, b), do: gcd(b, rem(a, b))
end
```

Wow, I was surprised, when you are used to it immediately your brain wire up the conditions and say "ah ok, we need this escape condition" or "we need to cover this pattern", the version in OCaml is very similar as well:

```ocaml
let rec gcd a, b =
    if b = 0 then a else gcd b (a mod b)
;;
```

Probably is just me, but I like the way we can express a lot easier math concepts in a functional programming language. (Yes, I know, I am probably late to the party).