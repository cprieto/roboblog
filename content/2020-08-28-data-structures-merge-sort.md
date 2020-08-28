---
title: Data structures, Merge sort
date: 2020-08-28
tags: theory, data structures, kotlin, algorithm
slug: data-structures-merge-sort
---

Merge sort is one of those algorithms that we kind of use everyday (most of the time indirectly or in a modified version) and we probably don't think about it. As I mentioned previously [quicksort]({filename}/2020-08-27-data-structures-quicksort.md) is kind of the facto sorting algorithm in many of standard library implementations in many languages but surprisingly [Merge sort]() is there as well. This is another [divide and conquer]() and recursive algorithm, and the idea is extremely simple:

> You divide a list until they are sorted (one element) and then merge them back while sorting them

So at the end what you do is to divide into smallest sublist and when merging you take care of sorting them back. In pseudocode it looks very familiar to the previous quick sort:

```psuedocode
function merge_sort(items, lo, hi)
  if low < hi then
    mid = lo + floor((lo + hi) / 2)
    merge_sort(items, lo, mid)
    merge_sort(items, mid + 1, lo)
    
    merge(items, lo, mid, hi)
  end
end
```

Again, converting this into Kotlin is simple enough:

```kotlin
import kotlin.math.floor

tailrec fun <T: Comparable<T>> mergeSort(items: MutableList<T>, low: Int = 0, high: Int = items.size - 1) {
  if (low >= high) return

  val mid = low + floor(((low + high) / 2).toDouble).toInt()
  mergeSort(items, low, mid)
  mergeSort(items, mid + 1, low)

  // This is where magic happens!
}
```

This is one specific thing I dislike from quicksort and merge sort, the real _core_ of the algorithm is _always_ hidden in some magic box, in quicksort was the `partition` section, here is the `merge` section. The guarantee is to take both divisions (or halves) and merge them back _but in sorted order_ and I remembered for me that was like "oh yeah, do you want fries with that?".

The easiest way is using an intermediary array, you see, we take both arrays (or array sections) and create a third array that will fit both arrays in memory and then place the sorted items there, sadly, with really big list you end up with a lot of wasted space because creating all those intermediary arrays and all the cost of copying the data back to the original array, nearly every implementation that I had seen out there was using this method but thanks to the great book ([Algorithms by R. Sedgewick](https://algs4.cs.princeton.edu/home/)) I saw a very clever way to do the merge operation in place! no memory wasted! (and personally a lot easier to follow and understand).

```pseudocode

```
