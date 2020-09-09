---
title: Data structures, Binary trees, breadth-first traversal
date: 2020-09-11
tags: theory, data structures, kotlin, algorithm
slug: data-structures-binary-trees-breadth-first-traversal
status: draft
---

We have not finished with trees yet! oh no! trees are one of the most versatil data structures out there in the wild. Last time we were taking a look at how to _visit_ or _traverse_ all the nodes in a tree and we saw [depth-first traversal](), but what if we want to visit _the same tree_ as last time but from top to bottom and left to right? (in this case generating the order `A, B, C, D, E, F, G, H`). Well, this type of traversal is named _breadth-first traversal_ or _level order_ traversal.

The easiest way to implement a level order traversal is using an additional data structure, a queue. The idea is simple, we start from the root and then add left and right to a queue and pops the queue until no element is present, nothing really exotic here:

```kotlin
fun levelOrder(operation: (T) -> Unit) {
  val queue = Queue<Node<T>>()
  queue.add(this)
  while (!queue.isEmpty()) {
      val elem = queue.pop()
      operation(elem.data)

      elem.left?.let { queue.push(it) }
      elem.right?.let { queue.push(it) }
  }
}
```

As previous blog post we add this method to the `Node` class. Notice the usage of a `Queue` structure, you can use the one implemented in the [simple queue blog post](). As with depth-first traversal there could be variations of the order you visit the nodes but in general it will be always from top to bottom and left to right.

This is easily tested with this simple method (you can add it to the previous unit tests for tree traversal):

```kotlin
@Test
fun `lever-order traverse`() {
  val result = mutableListOf<Char>()
  root.levelOrder { result.add(it) }

  assertEquals(listOf('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'), result)
}
```
