---
title: Data structures, Merge sort
date: 2020-09-01
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
fun <T: Comparable<T>> mergeSort(items: MutableList<T>, low: Int = 0, high: Int = items.size - 1) {
  if (low >= high) return

  val mid = low + (high - low) / 2
  mergeSort(items, low, mid)
  mergeSort(items, mid + 1, low)

  // This is where magic happens!
}
```

This is one specific thing I dislike from quicksort and merge sort, the real _core_ of the algorithm is _always_ hidden in some magic box, in quicksort was the `partition` section, here is the `merge` section. The guarantee is to take both divisions (or halves) and merge them back _but in sorted order_ and I remembered for me that was like "oh yeah, do you want fries with that?".

The easiest way is using an intermediary array, you see, we take both arrays (or array sections) and create a third array that will fit both arrays in memory and then place the sorted items there, sadly, with really big list you will have to deal with a lot of space (we will see more about this later), thanks to the great book ([Algorithms by R. Sedgewick](https://algs4.cs.princeton.edu/home/)) I saw a very clever way to do the merge in a very easy way to understand (compared with other books I had read about it):

```pseudocode
function merge(items, lo, mid, hi)
  i = lo
  j = mid + 1
  aux = []
  for k = lo to hi
    aux[k] = items[k]
  end

  for k = lo to hi
    if i > mid then
      items[k] = aux[j++]
    end
    if i > hi then
      items[k] = aux[i++]
    end
    if aux[j] < aux[i] then
      items[k] = aux[j++]
    else
      items[k] = aux[i++]
    end
  end
end
```

In this case we copy the data from the gap between low to high into an intermediary array and then go through the whole segment and checking against the current value using two pointers, one for each of the sides of the merge operation (that is what we see in that huge switch statement). Now with this implementing the merge operation in Kotlin is a piece of cake!

```kotlin
fun <T : Comparable<T>> mergeSort(items: MutableList<T>, lo: Int = 0, hi: Int = items.size - 1) {
    fun merge(lo: Int, hi: Int, mid: Int) {
        var a = 0;
        var b = (hi - mid) // b is the middle point of the collection
        val aux = items.slice(lo..hi) // We copy the part we need to sort

        for (idx in lo..hi) {
            items[idx] = when {
                a >= (hi - mid) -> aux[b++] // No remaining elements in the left side
                b >= aux.size -> aux[a++] // No remaining elements in the right side
                aux[a] < aux[b] -> aux[a++]
                else -> aux[b++]
            }
        }
    }

    if (hi <= lo) return // No elements to process, list already sorted!

    val mid = lo + (hi - lo) / 2
    mergeSort(items, lo, mid)
    mergeSort(items, mid + 1, hi)

    merge(lo, hi, mid)
}
```

Notice I am not marking the function `tailrec` because, well, it is not tail recursive. The `when` clause could be heavily simplified but I preferred to leave it like that so it is a lot clearer how the sorting process is done (it actually took me a while to digest and write the code but it felt good getting there by myself). As you see there is a big problem with our merge sort, we have to create an array of the size of the collection we are sorting, can you figure out why? (go, think about it).

Because we split the sorting collection in half all the time, the time performance of merging sort is pretty good, $\mathcal{O}(n \log{n})$, but at a high cost (temporary memory) for big collections. There is a big exception for all of this though, this algorithm becomes extremely memory efficient when dealing with linked lists (remember our friends [linked lists]({filename}/2020-08-14-data-structures-simple-single-linked-lists.md)?), in fact, this is the algorithm used by things like the Linux kernel to sort linked lists (because its efficiency with them). Go and try to write a version to sort linked lists instead of this array version, you will see what I am talking about.

There is _another_ way to write this sorter, besides using a linked list, and use a full recursive implementation passing lists and generating a new list all the time. It is actually a lot easier than this implementation, maybe in another blog post I will examine this case.

This was, for me, the hardest of all the sorting algorithms to write, I can't exactly tell you why, maybe it is the easiest for you, go and try writing it by yourself in your favourite programming language!