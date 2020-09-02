---
title: Data structures, quicksort
date: 2020-08-27
tags: theory, data structures, kotlin, algorithm
slug: data-structures-quicksort
---

Now it is time for the sorting algorithm that a lot of people says once you know it you don't need anything else (that is not really true in practice but who am I to judge them?), the venerable [Quicksort](https://en.wikipedia.org/wiki/Quicksort). This algorithm, discovered by [Sir Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare), is so effective that many of the default sorting algorithm in the standard library use it, a good example, that is why `qsort` exists in the C standard library.

This algorithm is the typical [_divide and conquer_](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) type of person, it basically picks an element (which is called _pivot_) and place all the elements greater than him in the right, and those lesser than him in the left, once this is done, you pick another element in the left and in the right and apply the same algorithm recursively until you end up with a sorted collection.

```pseudocode
function quicksort(items, low, high)
  if low < high then
    pivot <- partition(items, low, high)
    quicksort(items, low, pivot - 1)
    quicksort(items, pivot + 1, high)
  end
end
```

As you see this is very a recursive and very simple algorithm but there is one part that is cleverly hidden in the pseudocode, the partition algorithm. The partition algorithm is basically the one that makes all the hardcore work, it picks an element (this is actually more complex that it sounds), in fact, without the partition function our sorting is useless. This function needs to get the pivot element and then place all the elements greater than it to the right or lesser than it to the left.

Let's start implementing the core of the recursive function in Kotlin, we will discuss more about the partition function later, there are many options to see there!

```kotlin
tailrec fun <T: Comparable<T>> quickSort(items: MutableList<T>, low: Int = 0, high: Int = items.size - 1) {
  if (low >= high) return

  val pivot = partition(items, low, high)
  quickSort(items, low, pivot - 1)
  quickSort(items, pivot + 1, high)
}
```

If you don't care about memory one easy way to do this is just _generating an array of the same size as the original_ and start filling it putting the smaller elements in the left and the greater elements in the right and placing the pivot in the space left after the operation, then simply copy the array into the original array and done. The problem I see with this approach is the use of memory, we need to create a temporary array as big as the current array being processed and for me that is a waste of space! Can we do a swap in place? yes we can, for example, if we use the first element as pivot the pseudocode will be something like this:

```pseudocode
function partition(items, low, high)
  p <- items[low]
  i <- low + 1
  for j = i to hi do
    if items[j] < p then
      swap items[j], items[i]
      i = i + 1
    end
  end
  swap items[low], items[i - 1]
  return i
end
```

Apparently there are problems when chosing the first element as the pivot value (as a mention before, this is the secret sauce with quicksort, chosing the right pivot value) because when the elements are already (or nearly) sorted we have to do a lot of work, [Sedgewick](https://en.wikipedia.org/wiki/Robert_Sedgewick_(computer_scientist)) and others advice to instead use the _last element_ in the list (in reality he says we should use the median of the first, last and middle but that is too long to see for a short blog post). Knowing this we can change and adapt our partition function pseudocode:

```pseudocode
function partition(items, low, high)
  p <- items[high]
  i <- low
  for j = i to high do
    if items[j] <= p then
      swap items[j], items[i]
      i = i + 1
    end
  end
  swap items[high], items[i]
  return i
end
```

As you see not many things changes and that is good, we just took care of the indices in the first partition versus the second. I know it is difficult to see the move and swaps of elements but I will highly advice to write the code in something that you feel comfortable with and place a log or print at the end of the loop displaying the current status of the list, you will then see what elements move and the values of $i$ and $j$, low tech but effective!

Knowing this implementing the partition function in Kotlin is easy, let's do the partition function as an inner function (to reduce the space in the post):

```kotlin
fun <T: Comparable<T>> quickSort(items: MutableList<T>, low: Int = 0, high: Int = items.size - 1) {
  fun partition(low: Int, high: Int): Int {
    val current = items[high]
    var idx = low

    for (j in idx until high) {
      if (items[j] <= current)  {
        items[j] = items[idx].also { items[idx] = items[j] }  // This is how you do the a,b = b, a in Kotlin
        idx += 1
      }
    }
    items[high] = items[idx].also { items[idx] = items[high] }
    return idx
  }

  if (low >= high) return

  val pivot = partition(low, high)
  quickSort(items, low, pivot - 1)
  quickSort(items, pivot + 1, high)
}
```

Yes, I admit the code in Kotlin looks "weird" but you can test it with the same unit tests we have for all our sorting examples, in fact, a good idea will be to pass the `partition` function as a parameter (with a sensitive default) and implement both partition schemas (or try some other from the Wikipedia page) and create unit tests around them.

Why all of this mess? well, quick sort is, how I say this, **quick**! and it gets us a worst case of $\mathcal{O}(n^2)$ (not different than all the other _comparisson algorithms_) but in the best case we get up to $\mathcal{O}(n \log{n})$ or $\mathcal{O}(n)$ (depending on the partition function) no matter the size of your collection. There is one specific case when quicksort is as slow as any other sorting algorithm by comparisson ($\mathcal{O}(n^2)$), when we have a collection with very few repeated elements, for example something like this: `[1, 1, 5, 1, 12, 12, 12, 5, 5, 5, 5, 1, 12, 1, 12, 1, 1, 12, 1, 5]`, can you spot why?

|                                         | Comparisson        | Swaps                    |
|-----------------------------------------|--------------------|--------------------------|
| Best case (using good pivot)            | $\mathcal{O}(n)$   | $\mathcal{O}(n \log{n})$ |
| Worst case (a lot of repeated elements) | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$       |

This is why is so important to _at least_ know your sorting algorithms, not a single algorithm applies to every situation. We will see more of this in the upcoming blog posts (we will continue with sorting for a while). 

Runnable snippet for this code: [https://pl.kotl.in/3fXRcrTqB](https://pl.kotl.in/3fXRcrTqB)
