---
title: Data structures, Binary search, recursive
date: 2020-08-24
tags: theory, data structures, kotlin, algorithm
slug: data-structures-binary-search-recursive
---

Last time we took a look at the two simplest and basic search algorithms, [binary and linear search]({filename}/2020-08-19-data-structures-binary-and-linear-search.md), and I mentioned at the end that binary search is a good example of an algorithm that can be expressed in recursive way (and even analyzed its performance using the master theorem). I am pretty sure by now you already wrote the same algorithm using a recursive approach but just in case we will check a simple recursive algorithm for binary search.

When writing a recursive algorithm we need to take care of a few cases, especifically one important case, the case when we need to _exit_ from our recursive call (called the _base case_), this is basically the hardest part of writing a recursive algorithm because we need to think _when we should not be calling ourselves anymore_.

Let's take a look at the previous binary search algorithm, we know we have reached the end when we return `-1` but when does that happen? in the previous code snippet when we are **not** in the block marked by the condition `start <= end` (and well, the negation of that is `start > end`), we can mark this as our base case and because we modify those variables let's pass them as parameters to our function. At the end we will end up with something like this:

```kotlin
import kotlin.math.floor

tailrec fun <T : Comparable<T>> recursiveBinarySearch(
    items: List<T>,
    what: T,
    start: Int = 0,
    end: Int = items.size - 1
): Int {
    val middle = (end + start) / 2
    return when {
        start > end -> -1  // This is the base case
        items[middle] > what -> recursiveBinarySearch(items, what, low, middle - 1)
        items[middle] < what -> recursiveBinarySearch(items, what, middle + 1, high)
        else -> middle // This is the success case
    }
}
```

Calling the function is very easy: `recursiveBinarySearch(listOf(1, 2, 3, 4, 5), 12)` and we can reuse the same tests as for binary search.

We could say that in my implementation we have many "cases" (after all, we are using a `when` instruction) but in reality we only have the conditions to return if we _fail_ (the base case), the condition to return if we _succeed_ (we found the element) or continue calling the recursive function if we still have no idea if we should fail or continue (the other two conditions). Because we are passing the parameters required to the function to work and not depending on the result of the previous recursive call the compiler can throw away the stack of the current call and continue with the next call, this type of execution is called a [tail call](https://en.wikipedia.org/wiki/Tail_call) (recursive functions without tail call optimization are known for error messages like "your stack size is too big" or something similar). Functions using tail call are sometimes called _tail recursive_.

In the case of Kotlin is a good idea to add the `tailrec` modifier to the function, this doesn't make the function automatically tail recursive but the compiler will throw an error telling us that our function _is actually not tail recursive_. In [Scala](https://www.scala-lang.org/), for example, you could decorate the function with `@tailrec` instead.

I highly advice to every developer to try to think about recursive algorithms and data structures everytime they can, but don't get desperate and try to make _every_ data structure or algorithm recursive, remember, what matters at the end is simplicity and the fact it just works.
