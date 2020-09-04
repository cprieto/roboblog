---
title: Data structures, Bucket sort
date: 2020-09-03
tags: theory, data structures, kotlin, algorithm
slug: data-structures-bucket-sort
---

I promise this is the last sorting algorithm (for now)! and this time we have another non comparisson sorts (or well, not exactly but I will explain later). [Bucket sort]() is pretty much as it sounds, putting things into _buckets_ of data that are in an specific order. The idea is creating categorized buckets of data and then place the elements from the original collection into those buckets using a classification function, this is where it gets super tricky, a good classification function will place the elements in an evenly manner, for example the list:

```
[243, 637, 371, 598, 442, 137]
```

The values are evenly distributed and can be placed in 6 buckets using the distribution formula $\lfloor\frac{x}{100}\rfloor$ but if we try the same buckets with different not evenly distributed elements like this list:

```
[243, 637, 271, 698, 442, 137]
```

We will have two or more elements in the same bucket (in this case 243, 271 in bucket 2 and 637 and 698 in bucket 6). When this happens we do a simple trick, we place the elements in the same bucket and sort that small list using a simple comparisson sorter, like insert sort. This is why bucket sort is not entirely a non comparisson sort because sooner or later you will end up using a comparisson sort to sort elements in the same bucket. A simple way to calculate the correct bucket is create as many buckets as elements and then use the simple formula $\lfloor\frac{x\times\mathit{length}}{\mathit{max}}\rfloor$ where $\mathit{length}$ is the length of the collection (in our sample $6$) and $\mathit{max}$ the max number in the collection (in our sample $637$).

Thanks to this the implementation is pretty simple:

```kotlin
fun bucketSort(
    items: MutableList<Int>,
    max: Int,
    buckets: Array<MutableList<Int>> = Array(items.size) { mutableListOf() },
    position: (Int) -> Int = { x: Int -> (x * items.size) / max }
) {
    // Place each element in a bucket, this depends of the type of data
    for (elem in this) {
        val pos = position(elem) - 1
        buckets[pos].add(elem)
    }

    // Now we relocate all the elements back
    var idx = 0
    for (bucket in buckets) {
        if (bucket.isEmpty()) continue

        // We use insert sort because, well, it is small and simple
        bucket.insertionSort()

        for (elem in bucket) items[idx++] = elem
    }
}
```

Be careful, there could be cases where all your elements or most of them end up in the same sort! that is a problem because basically your sorter is doing nothing to simplify your life and you will be probably better with another sorter. How good is our sorter? well, it depends on what is the internal sorter that we use, in our previous case we know the worse case scenario for insertion sort is $\mathcal(O){n^2}$ and we have to go through all the elements and buckets in the collection, so it will be around $\mathcal{O}(n + k)$ where $k$ is the worst case for the internal sorter (for insertion sort we can say the worst case will be $\mathcal{O}(n + n \log{n})$). If the collection is evenly distributed it means every element is in its own bucket, so the time is reduced to $\Theta(n)$.

The unit tests for our sorter is similar to the previous used for radix and count sort, so feel free to copy the test.

**PD:** As with radix and counting sort, this is a very specialized sorter thanks to the buckets and positioning algorithm, it is (in concept) very similar to counting sort and in most implementations of radix sort they use buckets but without sorting (using linked lists), so keep that in mind when implementing this sorter from scratch.
