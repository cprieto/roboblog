---
title: The vector class, structured binding
date: 2021-05-17
slug: the-vector-class-structured-binding
tags: c++, native, programming
twitter_image: structured-binding.png
---

Last blog post we were talking about how to make a nicer vector class and extend it to handle an arbitrary number of components so it is easy to do things like `vector<3> v{1, 2, 3}` and saw how powerful is to use things like [traits](https://en.cppreference.com/w/cpp/header/type_traits) and [templates](https://en.cppreference.com/w/cpp/language/templates) in our C++ code to let the compiler do its job. Though everything is nice and fantastic, we face a problem with our vector class: In the past it was easy to get the `x` component because it was just a public member in our class and now we have to deal with indexes, that is not "optimal".

Fortunately we are dealing with C++17 and there is another compiler help we can take advantage of, [structured binding](https://en.cppreference.com/w/cpp/language/structured_binding), if you are used to work in Javascript or Python you will understand what I am talking about, instead of doing things like:

```c++
vector<3> v{1, 2, 3};
auto x = v[0];
auto y = v[1];
auto z = v[2];
```

We can request a simpler way to get the same values:

```c++
vector<3> v{1, 2, 3};
auto [x, y, z] = v;
```

# In the wild...

The specification states that if your member fields are already public you don't need to do anything special, so this sample will work without any changes at all:

```c++
struct vector {
    float x, y, z;
    explicit vector(float x, float y, float z): x{x}, y{y}, z{z} {}
};

vector v{1, 2, 3};
auto [x, y, z] = v;
```

And this is because a struct has all its members public _by default_ so `x`, `y`, and `z` can be easily destructured later. Easy, isn't it? but well, sadly that is **not** our case, our `elements` array is private and it makes no sense to make it public.

# Implementing structured binding in our class

There are many guidances out there to do this (I will point to those at the end) but long story short there are only three things to implement.

First we need to tell the compiler _what is the size_ of our results in the expression, in this case is 3 because, well, we have 3 members (`vector<3>` has 3 components and `vector<2>` has only 2). To tell the compiler this information we need to create the `struct` [`std::tuple_size`](https://en.cppreference.com/w/cpp/utility/tuple/tuple_size), the easiest way is to just inherit from the type trait [std::integral_constant](https://en.cppreference.com/w/cpp/types/integral_constant):

```c++
template<std::size_t N>
struct std::tuple_size<vector<N>>: std::integral_constant<std::size_t, N> {};
```

Notice we use a template parameter `N` because we don't really know what type of vector it is, and then use later that parameter as the given size that we use when using `std::integral_constant`. Nothing fancy here.

Second we need to tell the compiler _the types_ of the values we will be returning, as with `std::tuple_size` we have to implement another `struct`, in this case is [`std::tuple_element`](https://en.cppreference.com/w/cpp/utility/tuple/tuple_element), this implementation is a little different, it will pass the index of the element the compiler needs to know the type and you just return the type. You can do nifty tricks to optimize this implementation and as with all the other members, it depends a lot of _what is your intent_ when destructuring. For us is simple, we know we _always_ will return `float`:

```c++
template<std::size_t Idx, std::size_t N>
struct std::tuple_element<Idx, vector<N>> {
    using type = float;
};
```

Third and final, we have now to implement a public member function in our class, yes, previous steps involved implementing things that were not members in our type, now it is type to do the only required member function, it is called with a not very exciting name, `get`. It sounds hardcore but you will see how simple it is to implement in our specific case:

```c++
template <std::size_t Idx>
[[nodiscard]] float get() const {
    return elements.at(Idx);
}
```

See? nothing super complex, very simple and straighforward! Just remember this is a member function (it has to be _inside_ your class definition).

Good readings for this subject are the [blog post](https://devblogs.microsoft.com/oldnewthing/20201015-00/?p=104369) by [Raymond Chen](https://devblogs.microsoft.com/oldnewthing/) and [another blog post](https://blog.tartanllama.xyz/structured-bindings/) by [Sy Brand](https://twitter.com/TartanLlama).
