---
title: Data structures, Counting sort
date: 2020-09-02
tags: theory, data structures, kotlin, algorithm
slug: data-structures-counting-sort
---

Ok, today we have another sorting algorithm but "_different_" not only in idea and implementation but in usage. So far we have seen _comparison sorts_ or sorting algorithms depending on comparing elements against each other (yes, some of them even recursive and divide and conquer). One big limitation of comparison sorts is that it doesn't matter what we do to improve them, the worst case would never be better (or faster) than $\mathcal{O}(n \log{n})$. Most algorithm classes stop in comparison sorts so I was surprised when I learnt about _non comparison sorts_ or sorts that doesn't use comparisson to sort the elements. Because of that, non comparisson sorts can do _much better_ than $\mathcal{O}(n \log{n})$ but with the disvantage that they can sort just certain domain of elements.

The first non comparisson sort we are going to check is the simplest of them. It is [counting sort](https://en.wikipedia.org/wiki/Counting_sort) and it is designed to work on a collection of _repeated discrete limited_ elements. This means collection containing repeated elements that we can enumerate, for example:"

- Family of integers: [1, 5, 1, 3, 1]
- Enums: [up, up, down, down, left, right, left, right]
- Letters: ['y', 'z', 'y', 'x', 'x', 'z']

The domain of sorting elements (enumerable) and limited number of elements is important because the way the algorithm works, it needs to know what is the _greater_ element in the list to sort. The functionality is really easy to explain:

- Create a temporary array with size up to `max` of the elements
- Go through each of the original elements, for each of the elements sum one to the index of the temporary array we just created
- Go through all the elements in the copy of the array, if the contained number is greater to 1, place the element and repeat until the number of elements is zero

In code is easy to do in Kotlin, contrary to the previous implementations, we will use a mutable list of integers to simplify the implementation:

```kotlin
fun countSort(items: MutableList<T>, max: Int) {
    val counter = Array<Int>(max + 1) { 0 } // This is because we need an array containing up to max

    items.forEach { counter[it]++ }

    var pos = 0
    for (idx in counter.indices) {
        while (counter[idx] > 0) {
            items[pos++] = idx
            counter[idx]--
        }
    }
}
```

This, of course, requires a different test:

```kotlin
import kotlin.test.*

class CountSortTests {
    private val expected = listOf(1, 1, 1, 3, 5)

    @Test
    fun `It sorts a list of integers`() {
        val items = mutableListOf(1, 5, 1, 3, 1)
        countSort(items, 5)
        assertEquals(expected, items)
    }

    @Test
    fun `It does nothing in an already sorted list of integers`() {
        val items = expected.toMutableList()
        countSort(items, 5)
        assertEquals(expected, items)
    }
}
```

Check the code and you will see we have to go through the list just _twice_, in other words, the time performance would be something like $T(n) = 2nC_a + C_b$ that can be represented with a case of $\Theta(n)$, there is no worst or best case, we will always have to go through all the elements in the list (that is why is good to use $\Theta$ here for time performance notation). If you think about this algorithm you will quickly realise that it can be used to _remove repeated elements_ and generate a new shorter list with unique elements, all of this at $\Theta(n)$ speed ;) try to modify the algorithm to return a sorted list of unique elements instead of just sorting them in place.

This is one of the few algorithms that you will probably have to implement by yourself, mostly because the logic regarding enumerating the elements and placing them in the correct place or order in the temporary container.
