---
title: The vector class, constructors and templates
date: 2021-05-12
slug: the-vector-class-constructors-and-templates
tags: c++, native, programming
twitter_image: templates.png
---

While reading the fantastic book [Foundations of Game Engine Development, Volume 1: Mathematics](https://foundationsofgameenginedev.com/#fged1) by [Dr. Eric Lengyel](http://terathon.com/lengyel/) and working through his examples I found the venerable `vector3d` class, a simple class to handle 3D vectors. I decided to try something different and write a slightly different version of the 3D vector class in C++, for my surprise it was not as trivial as I initially thought so I decided to write a short blog post series about my adventures in the land of modern C++.

# A better constructor
​
The first change I did was to support arbitrary length of vectors, so instead of using a "fix it all" `vector3d` class I can use a variable length vector. To simplify its implementation I decided to use a `std::array` container internally so our simple class will look like this:
​
```c++
template<std::size_t N>
class vector {
  std::array<float, N> elems;
public:
  vector() = default;
}
```
​
What if I want to specify the values in the constructor? for example, I would love to do something like this:
​
```
vector<3> v{1, 2, 3};
```
​
My first impulse was create a constructor using an `std::initializer_list` :
​
```c++
vector(std::initializer_list<float>)
```
​
But this will kind of mess with our internal `std::array` and I really don't want to change the container to a component like `std::vector` and there is no challenge doing this, it will be to easy so I decided to take a different path.
​
What if I use something like [variadic template arguments?](https://eli.thegreenplace.net/2014/variadic-templates-in-c/)
​
# Use a template they said, it will be fun they said...

Let's try to implement a variadic template to solve our constructor problem:

```c++
template<std::size_t N>
class vector {
    std::array<float, N> elems;
public:
    vector() = default;
    template<typename... Args>
    explicit vector(Args... args): elems{{args...}} {}
}
```

And just like nothing we have our simplest case working! Though, you could notice a few problems, what if I pass more than 3 arguments in a `vector<3>`? what if I pass 2?

```c++
vector<3> a{1, 2, 3};  // Works!
vector<3> b{1, 2};  // Oops, this should fail
vector<3> c{1, 2, 3, 4}; // This should fail too!
```

We could try to check the length of arguments and throw an exception, simple, right?

```c++
template<typename... Args>
explicit vector(Args... args): elems{{args...}} {
    if (sizeof...(Args) != N) {
            throw std::invalid_argument("oops!");
    }
}
```

This does the job but at what cost? the exception and error was thrown _at running time_ and this is not really what we are trying to do. If you think about that, we already have _enough information_ to know if we are using the constructor correctly (the vector size) so we could fail _at compile time_ and not waiting to fail at running time. One simple way to achieve the same at compile time is our old friend [`static_assert`](https://en.cppreference.com/w/cpp/language/static_assert), let's change the constructor a little:

```c++
template<typename... Args>
explicit vector(Args... args): elems{{args...}} {
    static_assert(sizeof...(Args) == N);
}
```

It works and now when trying to compile our compiler will scream back at us saying we are breaking the assertion, the size of our passed arguments is not the same as the nontype template argument.

# Can we do better?

I started thinking how can we do this better? I mean, it is nice for having a compiler telling us we are trying to cut our limbs but can you be a little more explicit when telling me I am doing it wrong? I approached some C++ experts and they gave me an idea! What if, listen to me, we _enable_ that constructor _only if_ we pass the correct number of arguments to it?. This sounds magical but thanks to the magic of templates is possible to do it with our pal [`std::enable_if`](https://en.cppreference.com/w/cpp/types/enable_if) and its friends.

I am not going to bore you with the details (check the reference and I will give you a few readings at the end) but we can simplify our constructor to something like this:

```c++
template<typename... Args, typename std::enable_if_v<(sizeof...(Args) == N)>* = nullptr>
explicit vector(Args... args): elems{{args...}} {}
```

Yes, it looks like a weird template definition but we are basically saying to enable a type _only if_ the condition `sizeof...(Args) == N`, if this condition is not met the template is disabled and our constructor is never there. In an IDE like CLion the effect of this is amazing, now we get the error directly in the instance and not in the template, telling us there is no constructor to satisfy our demands!

# The perils of convertible types

Are we done yet? what happens when we pass float parameters and integer parameters? they should just work, right?

```c++
vector<2> a{1.0f, 2.0f}; // It works
vector<2> b{1, 2}; // It should work but it doesn't!
vector<2> c{1, 2.0f} // Why are you not working?!
```

I must confess I tried for a while to solve this problem and then a good user in the C++ slack channel point me the obvious:

```c++
template<typename... Args, typename std::enable_if_v<(sizeof...(Args) == N)>* = nullptr>
explicit vector(Args... args): elems{static_cast<float>(args)...} {}
```

Nice! now it will work with all of our previous examples!

Let's try something risky:

```c++
vector<2> x{1, "b"}; // This should fail
```

Well, this fails but not where we wanted it to fail! Our new shiny constructor is doing its job but not really, it is being enabled because we are passing two parameters but it should make sure those parameters _can be_ casted to a `float`. Looking around I saw many solutions but thanks to C++17 new [`std::conjuction_v`](https://www.fluentcpp.com/2021/04/30/how-to-implement-stdconjunction-and-stddisjunction-in-c11/) we can stop worrying about using some hacks and use it directly:

```c++
template<typename... Args, std::enable_if_t<sizeof...(Args) == N && std::conjunction_v<std::is_convertible<Args, float>...>>* = nullptr>
explicit vector(Args... args): elems{static_cast<float>(args)...} {}
```

This looks like a mouthfull in the constructor, so maybe it will be a good idea to simplify it a little:

```c++
template<std::size_t N, typename... T>
using vector_t = std::enable_if_t<sizeof...(T) == N && std::conjunction_v<std::is_convertible<T, float>...>>;

template<std::size_t N>
class vector {
    std::array<float, N> elems;
public:
    vector() = default;
    template<typename... Args, vector_t<N, Args...>* = nullptr>
    explicit vector(Args... args): elems{static_cast<float>(args)...} {}
};
```

And there you go, our nice vector class acts as we planned! You could add a few more additions to this template, for example, extend the template to use a type that is not `float` in case you know you want _only_ vectors to contain integers, for example.

# You want to know more?

I cannot stress enough how helpful has been the [C++ Slack channel](https://cppalliance.org/slack/) community, they really rock and they are amazing helping and answering questions to newbies like me. I heavily encourage you to reach them and participate in the channel if you are into C++ and all of that. Another amazing guide for templates has been the great book [C++ Templates, The complete guide](https://www.google.de/books/edition/C++_Templates/PM0lYAAACAAJ) by David Vandevoorde, this book has amazing content about how templates work and goes deep into implementation details, it is a must read if you are learning or already an expert in C++.

Now, if you want to know the history about templates and how did we get were we are right now I cannot recommend [From Mathematics to Generic Programming](https://dl.acm.org/doi/book/10.5555/2643027) by Alexander Stepanov, such an amazing book, not only for C++ developers but for anyone who wants to know more about generics and templates in general.

[C++20](https://en.cppreference.com/w/cpp/20) is out and one of the nice things is the addition of [concepts](https://www.modernescpp.com/index.php/c-20-concepts-the-details), these are template constraints, very similar to those found in languages like C# and Java and this is going to be something that will really improve metaprogramming and solving similar problems like this constructor but with less code and more help from the compiler, maybe soon I will rewrite my vector class to be C++20 aware, who knows!
