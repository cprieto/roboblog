---
title: Data structures, Radix sort
date: 2020-09-03
tags: theory, data structures, kotlin, algorithm
slug: data-structures-radix-sort
---

We return with another _special_ sorter, last time we saw [counting sort]({filename}/2020-09-02-data-structures-counting-sort.md) to sort a collection of repeated small limited number of ordinal discrete types and I mentioned its usage and how it can be extremely useful to sort such things. There are a few problems with our counting sort though, for example, what if you want to sort numbers like 916, 913, 15, 96? what about sorting a list of words in a dictionary? what if you want to sort a list containing lists? Yes, as you may already guessed we are talking about another special sorter here, the [radix sort](https://en.wikipedia.org/wiki/Radix_sort).

The idea is simple, we sort each element as separate digits, for example: `[613, 218, 350, 157, 108, 457]` will be sorted first using the last digit (`[350, 613, 157, 457, 218, 108]`) and then by the second digit (`[108, 613, 218, 350, 157, 457]`) and finally using the first digit (`[108, 157, 218, 350, 457, 613]`). Notice each time we pass we _preserve the relative order_ the elements are between each other, for example, after the first pass we keep `157` _before_ `457` and after the second pass we keep `613` _before_ `218`. This algorithm is stable and uses this as a way to keep and handle the sorting process, the order can be done from _least significant_ to _most significant_ number or totally the opposite, from _most significant_ to _least significant_, that won't alter the final product of the sort process.

The previous algorithm we saw (counting sort) was called like that because it depends on _counting_ each elements in the collection to sort them, so why is this one named _radix_? well, because it requires a [radix](https://en.wikipedia.org/wiki/Radix) or base to divide each element in its components, in the previous example the radix is of course 10 (the decimal system). This sorter doesn't do much by itself and internally it depends on a stable sorter, most implementations use counting sort to arrange each digit (or well, a simple modification of counting sort). It is a lot easier to explain with a sorting example:

 > Sort the list `[613, 218, 350, 157, 108, 457]` using radix sort

 Well, we know we have up to 3 digits and the radix is 10, we will sort from right to left. First we need to create an empty array of size `radix` and fill it with zeroes:

```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

Now we go from left to right with the first digit and place it in the correct place in the radix array (remember how counting sort works):

```
[1, 0, 0, 1, 0, 0, 0, 2, 2, 0]
```

This is where it is a little different, we start a cummulative sum on each digit with the previous element, so the array becomes something like this (soon you will see where is the magic):

```
[1, 1, 1, 2, 2, 2, 2, 4, 6, 6]
```

We are ready to place our elements in the original array, for this we need a temporary array to place the new located elements and this time we examine again each element but this time from right to left, starting with `457` (current digit: 7), if we check the position 7 in the radix array we see it has number 4, we place that element in the index 4 - 1 of the array (we substract one because in our cases indices in arrays and list starts at 0, not 1):

```
[0, 0, 0, 457, 0, 0]
```

We substract one in the radix array for that element:

```
[1, 1, 1, 2, 2, 2, 2, 3, 6, 6]
```

And we continue with the next, `108`, this one needs to go in the 5 position of the array (6 - 1 = 5):

```
[0, 0, 0, 457, 0, 108]
```

And we continue until we finished with the array and repeat the same process with the next element.

We can implement this as an _in-place_ sorter but this will make our sorter [_unstable_](https://en.wikipedia.org/wiki/Sorting_algorithm#Stability) so for simplicity I will go with a different sort mechanism and instead of implement it returning always a new list, this give us a big advantage as well, we can implement this algorithm as _recursive_ (we will use arrays to simplify the operation, but you get the gist):

```kotlin
tailrec fun radixSort(items: Array<Int>, digits: Int, current: Int = 0): Array<Int> {
  // This is the base case
  if (current == digits) return items

  val results = Array<Int>(items.size) { 0 }
  val locations = Array<Int>(10) { 0 }

  val power = 10.0.pow(current)

  // We do this to avoid repeating the same operation
  val position = { x: Int -> ((x / power) % 10).toInt() }

  // Normal counting sort
  for (elem in items) {
    val pos = position(elem)
    locations[pos]++
  }

  // This is the accumulative number for each location
  for (idx in 1 until locations.size) {
    locations[idx] += locations[idx - 1]
  }

  // Now we place each element in the correct place in the result
  for (idx in items.size - 1 downTo 0) {
    val elem = items[idx]
    val pos = position(elem)

    val loc = (locations[pos] - 1).also { locations[pos]-- }
    results[loc] = elem
  }

  // recursive call
  return radixSort(results, digits, current + 1)
}
```

Our sorter is even _tail recursive_! yay!

Ok, how good is our sorter? if you examine the code, we basically have to go through every element ($n$) the amount of _digits_ ($d$) and _radix_ ($r$) times the amount of digits, so it will behave something like this: $\Theta(dn + dr)$ or $\Theta(d(n + r))$ if you prefer.

This sorter is still really fast compared to any comparisson sort and it is fantastic for sorting lists, strings, in fact anything that you can think as a collection or that can be represented with a radix. For example, you could use it to sort genetic sequences where the _radix_ is 4 (because you only have 4 bases) or binary strings where your radix is 2.

Most of the time you will need to implement a radix sort from scratch but it worth the effort if your data can be sort super fast with this method.
