---
title: Data structures, Bubble sort algorithm
date: 2020-08-18
tags: theory, data structures, python, algorithm
slug: data-structures-bubble-sort-algorithm
---

Now it is time to make a pause in our basic data structures and start taking a look at some sorting algorithms. For simplicity these algorithms will be explained using an arrays or lists and it will be done in place (that means every sort will sort the container instead of returning a new one).

```python
def bubble_sort(elems: List[T]) -> None:
  """Sorts a list using the bubble sort algorithm, this is sort in-place"""
  if not elems:
    return

  for last in range(len(elems), 0, -1):
    for idx in range(1, last):
      if elems[idx - 1] > elems[idx]:
        elems[idx - 1], elems[idx] = elems[idx], elems[idx - 1]
```

The first algorithm we are going to take a look is one of those things that you should know but you should never use, the [bubble sort algorithm](https://en.wikipedia.org/wiki/Bubble_sort).

It is called because it will compare each element with the element next to it, if it is in different expected order they will swap and we will continue doing this until we reach the end (or beginning) of the list and then repeat until all the elements are sorted. If we start sorting from the beginning of the array, the last elements of the array will be in their correct position with each pass (or if they are sorted from end to beginning, the first elements of the list will be in the right order).

|                                 | Comparissons       | Swaps              |
|---------------------------------|--------------------|--------------------|
| Best case (list already sorted) | $\mathcal{O}(n)$   | $\mathcal{O}(1)$   |
| Worst case                      | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ |

Bubble sort is extremely inefficient because even when the list is already sorted we have to go through all the elements of the list to check they are sorted, so that means doing nnn comparissons, while in the worst case we will need to do as much as $n^2$ comparissons (and as you see in the previous code, that is the most expensive operation in our code and something that needs to happen all the time). Not in vain [Knuth](https://en.wikipedia.org/wiki/Donald_Knuth) said:

> In short, the bubble sort seems to have nothing to recommend it, except a catchy nameand the fact that it leads to some interesting theoretical problems

Should you ever use bubble sort for anything? the short answer is **no**, I like to think we learn about bubble sort because legacy and it is good to compare every other sorting algorithm with one of the worsts, in fact, I like to start with bubble sort when talking about complexity of algorithms because it is simple to realize by yourself why is so bad (I left you that as an exercise!).

Bubble sort is so very well known that there are even variants improving the algorithm, for example, an early exit of the loop when there is no swap (all elements are sorted) or alternating the sorting direction and operation, I left to you the idea about how to modify the current Python code to do both operations.

As usual I leave you with the testing code, this time using the amazing [pytest](https://docs.pytest.org/en/stable/) framework:

```python
expected = list(range(1, 100))

def test_bubble_sort():
    entry = random.sample(range(1, 100), 99)
    bubble_sort(entry)
    assert entry == expected
```

Sorting is one of those really interesting problems where we can see and study the complexity and elegance (or lack of it) for some algorithms, I quite like them.