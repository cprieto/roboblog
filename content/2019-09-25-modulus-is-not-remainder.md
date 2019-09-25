title: Modulus is not Remainder
date: 2019-09-25
slug: modulus-is-not-remainder
tags: programming, math

---
I know this has been explained many times in the past, but interestingly this bit me in the back a few days ago while coding, and, the same as _homogeneous coordinates_ we will find plenty of different explanations depending on whom we ask to.

Mathematically speaking, we define a _modulus_ or $a \mod n$ to be the remainder $r$ when $a$ is divided by $n$, in other words:

$$
r = a \mod n = \lfloor a/n \rfloor n
$$

This was defined by [Gauss](https://de.wikipedia.org/wiki/Carl_Friedrich_Gau%C3%9F) in 1801, thought the Chinese and Greeks probably knew about it thousand years before. One important thing about this is that $0 \ge r \lt n$.

This last part is important, because it defines a modulus as a positive number, for example:

$$
\begin{align}
35 \mod 12 &= 11\\
-129 \mod 7 &= 4
\end{align}
$$

Why the second case is 4? You could say the result is -3 (because the sign), but because we already establish that $0 \ge r \lt n$ the number cannot be negative, so we say $7-3 = 4$. We usually say _-129 is congruent with 4 mod 7_ or with the notation $-129 \equiv 4 \pmod 7$ which means both $-129$ and $4$ have the same remainders when divided by 7.

Notice, while we use the word _reminder_, the modulus is not the remainder, $-3$ is the remainder while $4$ is the modulus.

## And now computers...

Almost every programming language I had seen have the _modulus_ operator, most of the time is expressed by the percentage symbol, so `35 % 12` is the same as $35 \mod 12$. What about the operation against a negative number?

```js
-129 % 7 // Returns -3, it should return 4
```

What? This is true for JavaScript, Go, C/C++, C# (and potentially CLR languages like VB and F#), Java (and JVM languages like Scala, Kotlin), in fact, almost everywhere where they mention they support the _modulus_ operator in reality they implement the _remainder_ operator instead. Notice _a few languages_ have the decency of use the right language, for example, [Elixir](https://elixirschool.com/en/lessons/basics/basics/#arithmetic) name it remainder and not _mod_. In Ruby `%` is the remainder operator while `modulus` is the modulus operator.

The [Wikipedia page](https://en.wikipedia.org/wiki/Modulo_operation) has a good list and sort of explanation why this happens, but I can see in the same way as _homogeneous coordinates_ everybody says both are right conceptions, my math books disagree with them though.

We could assume every programming language uses the `%` as the remainder instead of the modulus? oh my friend, you will get a nice surprise when using Python and R, both operators (`%%` in R) are true modulus operators, so `-129 % 7` will return 4. And yes, they are named _modulus_ as well.

## Further readings

I highly recommend the Wikipedia page, at least for the list of implementations in different programming languages (notice some languages like C/C++ the sign is implementation specific, so it could be different depending on the compiler). [Rob Conery](https://rob.conery.io/2018/08/21/mod-and-remainder-are-not-the-same/) wrote a blog post some time ago about the same topic. If you want to go really down in the rabbit hole I recommend the section 1.6 _Theory of congruences_ from the book [Number Theory for Computing](https://www.amazon.com/Number-Theory-Computing-Song-Yan/dp/3540430725) by Song Y. Yang, its explanation is massive and very mathematical but it has been my guide for, well, number theory :smile:

