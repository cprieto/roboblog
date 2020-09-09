---
title: Data structures, Binary trees
date: 2020-09-09
tags: theory, data structures, kotlin, algorithm
slug: data-structures-binary-trees
---

So far we had seen _linear structures_, linked list, queues, stack, arrays, all of them are linear data structures with well defined operations. [Trees](https://en.wikipedia.org/wiki/Binary_tree) are our first _non-linear_ data structure and, as the name says, they are data structures that looks like a tree (or an inverted tree).

Each element in a tree is named a _node_ and the first node, the node at the top, is named _root_, a node can have none or more _children_ and each children has a _parent_, the "connections" between each node are called _edges_, nodes without children (with the exception of the root node) are called _leaves_, the number of edges from the root to a node is called the _depth_ of the tree and the distance between the longest path of a node to the root is called the _height_ of a node, so to know the height of a node or tree we count the number of nodes from that node to the root node (inclusive). In the image we see the node $D$ has a depth of 2 and the whole tree has a height of 4, nodes $H$, $I$, $E$, $F$ and $G$ are leaves.

![tree]({attach}/images/tree-1.png 'Simple binary tree')`

Depending on the maximum number of children per node we have different types of trees, the simplest is a tree where each node has a maximum of 2 children (binary trees) and we will be exploring them extensively in this and upcoming blog posts. There are trees where nodes have up to three children (ternary trees) and even 4 (quaternary) and 8 (octary) trees, in general we usually talk about $n$-trees but we will be limiting ourselves to binary trees for now.

A simple way to assemble a binary tree is with a simple structure to hold the `data` and references to its `left` and `right` children, something simple like this:

```kotlin
// We make it comparable to make our life easier later
class Node<T : Comparable<T>>(
    private val data: T,
    private var left: Node<T>? = null,
    private var right: Node<T>? = null
)
```

And we can represent a tree like the one shown in the image directly in code:

```kotlin
val root = Node('A',
    Node('B',
        Node('D',
            Node('H'),
            Node('I')),
        Node('E')),
    Node('C',
        Node('F'),
        Node('G'))
)
```

A full binary tree is a tree where _all the nodes_ have two or no children at all, the tree in the example _is_ a full tree. There is the concept of a _complete tree_ but we will discuss that one when we see another structure related to trees, the heap. The maximum number of nodes in a full binary tree of $l$ levels is given by the equation $2^l -1$.

There are many properties of a tree that are useful when handling data, but for now try to represent a tree in your favourite language, as you see it is nothing fancy!
