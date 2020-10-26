---
title: Data structures, Binary search trees
date: 2020-09-12
tags: theory, data structures, kotlin, algorithm
slug: data-structures-binary-search-trees
status: draft
---

I already mentioned trees are heavily used in the world of data structures and here we are again, with our first _specialized_ tree structure, the [binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree) (BST for short). A binary search tree is as any other trees but with one specific characteristic: The value in the left node is smaller that the root node and the value in the right node is greater than the value in the root node, this characteristic makes the tree really easy to navigate and search for values, you compare values and search at the right or left depending of the operation.

Overall a binary search tree has the following operations:

 - Insert a new element in the tree, this will involve deciding if we need to insert it at the left or right
 - Search for a value in the tree, thanks to the comparisson operations we can easily find a value in the whole tree
 - Delete a value in the tree, this is the most complicated operation, mostly because we need to make sure the "ordering" is maintained in the tree

Let's start with insert, because we need to compare elements we will make sure we restrict our generic to a comparable value:

```kotlin
class BNode<T : Comparable<T>>(
    private val data: T,
    var left: BNode<T>? = null,
    var right: BNode<T>? = null
) {
  fun insert(value: T) {
    if (value == data) return

    if (value < data) {
      if (left == null) left = BNode(value) else left?.insert(value)
    } else {
      if (right == null) right = BNode(value) else right?.insert(value)
    }
  }

  fun insert(values: List<T>) { values.forEach { insert(it) } }
}
```

Notice the calls to each of the nodes to do the insert, they will do the same until find the correct empty place to put the value. Doing a simple insert like this:

```kotlin
val tree = BNode(5)
tree.insert(listOf(1, 6, 12, 13, 22))
```

Will generate a tree with the following shape:

![tree]({attach}/images/tree-3.png 'Skewed binary search tree')

To search in the tree the same logic is applied:

```kotlin
fun exists(value: T): Boolean {
  return when {
    data == value -> true
    data > value -> left?.exists(value) ?: false
    else -> right?.exists(value) ?: false
  }
}
```

Because inserting and searching are done in a simple fashing and taking into account the value both operations are extremely fast, to be precise $\mathcal{O}(\log{n})$ in the best case for both operations, though there is a worse case of $\mathcal{O}(h)$ where $h$ is the height of the tree (or even in very bad cases, the number of elements). This will happen if we _always_ insert a value that is smaller or a set of values that are larger, that will skew the tree to the left/right and basically transform it into a linked list, removing all the advantages of a binary search tree.

Removing an element from the tree is a little more complicated because we need to check if when removing the element we will need to rebalance the tree (remember, the smaller values should go to the left and bigger to the right), in general we have the simple cases when removing:

 - The node that we have to remove is a leave, nothing to do here we just remove the tree (simplest case)
 - 

```kotlin
fun delete(value: T) {

}
```
