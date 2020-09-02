---
title: Data structures, Binary and linear search
date: 2020-08-19
tags: theory, data structures, kotlin, algorithm
slug: data-structures-binary-and-linear-search
---

Another problem that goes hand by hand with sorting is the classical searching problem (and sometimes they need each other to work) and as sorting there are a few algorithms to pick from (sadly not as many as with sorting though). In its simplest form we just go through a collection, checking if the element we are searching for is there and if found we return the index or another number to show we failed, maybe something that will look like this in Kotlin:

```kotlin
fun <T> linearSearch(items: Collection<T>, what: T): Int {
    // NOTE: yes, I know I could use indexOf or even better, indexOfFirst
    for ((idx, item) in items.withIndex()) {
        if (item == what) return idx
    }
    return -1
}
```

In the best case the element we are looking for is the first element in the collection so its time performance would be $\mathcal{O}(1)$ in the worst case scenario (let's say the element _is not_ in the list) we will need to go through all the elements, being this a $\mathcal{O}(n)$ operation (where $n$ is the number of elements in the collection).

|                                          | Comparissons |
| ---------------------------------------- | ------------ |
| Worst case (element not found)           | $\mathcal{O}(n)$  |
| Best case (element is the first element) | $\mathcal{O}(1)$  |

When the list is unsorted we cannot do much to improve the efficiency but a different situation happens _when the list is already sorted_, if that is the case we can split the collection in parts and check if the element is in any of the subparts, this is a good example of [_divide and conquer_](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) algorithms, we split the collection in smaller pieces and that will improve the time performance of our algorithm.

For a given _ordered_ collection:

1.  Take the element in the middle
2.  If the element is what we are searching for, we found it!
3.  If the element is _greater_ than what we are searching for, we should search in the left of the element (between the `start` and the `middle - 1` of the collection)
4.  If the element is _smaller_ than what we are searching for, we know the element should be in the right of the collection (between `middle + 1` and the `end` of the collection)
5.  Rinse and repeat until we get the element or report it is not in the collection

As you can see we divide the big collection in _halves_ with every pass and that is why is called [_binary search_](https://en.wikipedia.org/wiki/Binary_search_algorithm) (there are actually two different theories why is called like that but I prefer to say that it is because we divide the collection in two, see [this StackExchange question](https://cs.stackexchange.com/questions/42726/why-is-binary-search-called-binary-search)).

The most simplest implementation (based in Wikipedia page about it) could be something like this:

```kotlin
import kotlin.math.floor

fun <T: Comparable<T>> binarySearch(items: List<T>, what: T): Int {
    var start = 0
    var end = items.size - 1

    while (start <= end) {
        val middle = floor(((start + end)/2).toDouble()).toInt()
        when {
            items[middle] > what -> end = middle - 1
            items[middle] < what -> start = middle + 1
            else -> return middle
        }
    }
    return -1
}
```

How good is this? well, if we count the operations executed and assigning arbitrary constants $C$ we will get something like this:

$$
T(n) = T(\frac{n}{2}) + C_k
$$

Let's remember the general form of the [master theorem](<https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)>):

$$
T(n) = aT(\frac{n}{b}) + \Theta(n^d)
$$

It looks like something we can use!, we know $C_k$ is constant so that should be $\Theta(1)$ at the end of the equation, and the only way $C_k = 1$ is when we power it $0$, and $a = 1$:

$$
T(n) = T(\frac{n}{b}) + \Theta(n^0)
$$

This looks like the _second form_ of the theorem ($d = \log_b{a}$ or $0 = \log_2{1}$) so we simplify it to $\Theta(\log{n})$, voilá!

|                                            | Comparissons      |
| ------------------------------------------ | ----------------- |
| Best case (element is right in the middle) | $\mathcal{O}(1)$       |
| Worst case (element is not there at all)   | $\mathcal{O}(\log{n})$ |

I don't have to tell you $\log{n}$ is smaller than $n$ but if you have any doubt, go and check ;)

The test for both cases are simple enough:

```kotlin
class SearchTests {
    private val unordered = listOf(5, 12, 56, 0)
    private val ordered = listOf(0, 5, 12, 56, 105, 200)

    @Test
    fun `linear search returns index of existing item`() {
        val found = linearSearch(unordered, 12)
        assertEquals(1, found)
    }

    @Test
    fun `linear search returns -1 when not found`() {
        val found = linearSearch(unordered, 35)
        assertEquals(-1, found)
    }

    @Test
    fun `classic binary search returns the index of the found element`() {
        val found = binarySearch(ordered, 5)
        assertEquals(1, found)
    }

    @Test
    fun `classic binary search returns -1 when not found`() {
        val found = binarySearch(ordered, 2)
        assertEquals(-1, found)
    }
}
```

I found binary search a really nice algorithm to learn things like recursion, master theorem and divide and conquer techniques, I leave you as an exercise to write the recursive version of this algorithm in Kotlin (or your preferred learning language), I am pretty sure you will have a lot of fun!
