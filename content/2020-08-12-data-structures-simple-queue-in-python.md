---
title: Data structures, a simple queue in Python 
date: 2020-08-12
tags: theory, data structures, python
slug: data-structures-simple-queue-in-python
twitter_image: queue-1.png
---

I found a simple way to understand algorithms and data structures is just to take a look at the pseudocode and implement it in a language, I usually do that exercise with a few different languages and I had been studying data structures and algorithms for a few weeks, so as I reminder to myself I decided to publish a few of those in my blog so I don't forget :D

The [abstract data structure](https://en.wikipedia.org/wiki/Abstract_data_type) queue can be implemented in two simple ways:

 - Using a [vector (array)](https://en.wikibooks.org/wiki/A-level_Computing/AQA/Paper_1/Fundamentals_of_data_structures/Vectors), this will involve growing and shrinking the vector or implementing a circular queue (I will explore this later -maybe-)
 - Using a [linked list](https://en.wikipedia.org/wiki/Linked_list) (another data structure!)

In both cases we will need a way to point to the head and the tail of the queue, because, well, queues are [FIFO](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)) structures and we are only allowed to **add** elements to the _tail_ (back) and **remove** them from the _head_ (front).

![Simple fifo queue]({attach}/images/queue-1.png)

In code this looks a lot simpler, I will use Python's `list` to simplify the operation (notice I am using Python's [`typing`](https://docs.python.org/3.8/library/typing.html?highlight=typing#module-typing) support and Python's [dataclasses](https://docs.python.org/3.8/library/dataclasses.html?highlight=dataclasses#module-dataclasses)):

```python
from typing import Generic, List
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class Queue(Generic[T]):
    elems: List[T] = field(default_factory=list)
    
    def enqueue(self, elem: T) -> None:
        self.elems.append(elem)
        
    def dequeue(self) -> T:
        assert self.elems, "Queue is empty"
        return self.elems.pop(0)
        
    @property
    def isEmpty(self) -> bool:
        return len(self.elems) == 0

    def peek(self) -> T:
        assert self.elems, "Queue is empty"
        return self.elems[0]
```

see? nothing fancy. A simple test for our queue would look like this:


```python
import unittest

class TestSimpleQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_empty_queue(self):
        self.assertTrue(self.queue.isEmpty)

    def test_queue_is_not_empty(self):
        self.queue.enqueue(1)
        self.assertFalse(self.queue.isEmpty)

    def test_queue_can_dequeue(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEquals(self.queue.dequeue(), 1)
        self.assertEquals(self.queue.dequeue(), 2)
        self.assertTrue(self.queue.isEmpty)

    def test_queue_can_peek(self):
        self.queue.enqueue(1)
        self.assertEquals(self.queue.peek(), 1)
        self.assertFalse(self.queue.isEmpty)
        self.assertEquals(self.queue.dequeue(), 1)
        self.assertTrue(self.queue.isEmpty)

    def test_dequeue_or_peek_fails_if_empty(self):
        with self.assertRaisesRegex(AssertError, 'Queue is empty'):
            self.queue.dequeue()
        with self.assertRaisesRegex(AssertError, 'Queue is empty'):
            self.queue.peek()
```

I won't recommend to implement your own queue in Python _at least that you know why and what are you doing it_. Python _already_ has a not one but many general and specialized queue classes living in the [`queue`](https://docs.python.org/3/library/queue.html?highlight=queue#module-queue) package in the standard library, in fact, it offers asynchronous specialized queues as well in the [`asyncio`](https://docs.python.org/3/library/asyncio-queue.html?highlight=queue#asyncio.Queue) package, use those.
