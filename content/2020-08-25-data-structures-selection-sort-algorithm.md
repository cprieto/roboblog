---
title: Data structures, selection sort algorithm
date: 2020-08-25
tags: theory, data structures, python
slug: data-structures-selection-sort-algorithm
---

Do you remember I mentioned last time (in [bubble sort]({filename}/2020-08-18-data-structures-bubble-sort-algorithm.md)) that you should know about it but _never_ use it or implement it? well, it is time for the second sorting algorithm in the same cathegory, the [selection sort](https://en.wikipedia.org/wiki/Selection_sort) algorithm. The idea of the algorithm is pretty simple, instead of comparing every element with the element next to it now we compare one element with all the other elements to see which one is _smaller_ (or larger depending on your sorting order) and swap it. In other words, we take one element and swap it with the smallest element remaining in the list and do this until we go through the whole list. A simple implementation in Python would look like this (there could be a much better idiomatic way to write this but to simplify I will leave it in a _sort of pseudo code_ so it is easy to move to something like Go, C++, Java, etc.):

```python
"""Sorts a list in place using the selection sort algorithm"""
def selection_sort(items: List[T]) -> None:
  size = len(items)
  for i in range(0, size - 1):
    idx = i
    for j in range(i + 1, size):
      if items[idx] > items[j]:  # Set which one is the smallest index so far
        idx = j
    if idx != i:  # We swap values if needed
      items[i], items[idx] = items[idx], items[i]
```

As you see, we end up doing simple linear search for the max value between all the values remaining in the list after our current index, because of this, we can see this algorithm will need to do $n^2$ comparissons but up to $n$ swaps (while bubble sort was doing $n^2$ swaps and the same amount of comparissons):

|                             | Comparissons  | Swaps       |
|-----------------------------|---------------|-------------|
| Best case (already sorted ) | $\Theta(n^2)$ | $\Theta(1)$ |
| Worst case                  | $\Theta(n^2)$ | $\Theta(n)$ |

You can reuse the test case used for the bubble sort algorithm as well and the sorting is done in place (remember, lists are kind of _by-reference_ structures in Python). Try to implement it in any other language and see how it works. Have fun!
