---
title: Data structures, Insertion sort algorithm
date: 2020-08-26
tags: theory, data structures, kotlin, algorithm
slug: data-structures-insertion-sort-algorithm
---

So far we had discussed two algorithms that you _should never use_ (because there are better options) but today we are going to talk about one of those _basic_ algorithms that you should **definitely use** for very specific cases. We are talking about [insertion sort](https://en.wikipedia.org/wiki/Insertion_sort), one of those algorithms that if we look at its pseudocode it kind of look complex and weird:

```pseudocode
function insertion_sort(items[], length)
  for n <- 0; n < length; n++
    elem <- items[n]
    idx <- n
    for i <- idx - 1; i >= 0; j--
      if elem < items[i]
        items[i+1] = items[i]
        idx--
      end
    end
    items[idx] = elem
  end
end
```

But in reality the idea (and implementation) is not that complex, what we take an element (let's say the $i$ element in the list) and then compare it with all the _previous_ elements in the list, if that element is _greater_ than our current element, we move it (or push) to our current position (so the element at index $i - 1$ will be at index $i$) until we found a place $x$ where the current element is not greater or lesser than previous and next (so we found the element correct place in the array). This is analogous as the way we sort a deck of cards, we take one card and then look for the correct position of that card in the deck and _insert_ the card into that position, hence the name of this algorithm.

If we try this in something like Kotlin we will end up with a simple implementation like this:

```kotlin
fun <T: Comparable<T>> insertionSort(items: MutableList<T>) {
    for (current in 0 until items.size) {
        var idx = current
        val value = items[current]

        for (i in idx - 1 downTo 0) { // We compare with all the previous elements
            if (value < items[i]) {
                items[(i + 1)] = items[i] // If bigger, we move current element to the right
                idx -= 1 // And we continue checking the previous element
            }
        }

        items[idx] = value // This is the right place for the item in the list
    }   
}
```

I really hope this makes it a little clearer, it took a while for me! Apparently this algorithm is so simple that someone implemented it in C in just two lines! (check the Wikipedia page) but I am far away from that :D

If you check the flow of the algorithm, we only need $\Theta(n)$ comparissons and we only _swap_ the value if needed, that means that for _already sorted_ collections we have a best case with zero swapping! of course, if the list is completely unsorted (let's say, it is in the opposite sort order) we will take as many comparissons as swaps ($n^2$).

|                                     | Comparissons  | Swaps         |
|-------------------------------------|---------------|---------------|
| Best case (list is already sorted)  | $\mathcal{O}(n)$   | $\mathcal{O}(1)$   |
| Worst case (list is super unsorted) | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ |

Thanks to this, many standard library implementations have an insertion sort algorithm because this specific algorithm is fantastic when our collection is not really big and it is nearly or close to be sorted. Another reason this algorithm is still very used is that (as with bubble sort and many other algorithms) is _stable_, that means that it will preserve the existing order of adjacent elements after the sorting.

**PD:** Some of my coworkers suggested keeping the code in only one language, so from now on I will try to keep the code in Kotlin (I am forcing myself to improve at it) except that, for some reason, is needed in another language to make it clearer, thanks for reading my blog!
