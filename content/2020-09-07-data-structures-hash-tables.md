---
title: Data structures, Hash tables
date: 2020-09-07
tags: theory, data structures, kotlin, algorithm
slug: data-structures-hash-tables
---

Well, time to go back to data structures. So far we had seen [queues]({filename}/2020-08-12-data-structures-simple-queue-in-python.md), [stacks]({filename}/2020-08-17-data-structures-simple-single-linked-lists.md) and [linked lists]({filename}/2020-08-14-data-structures-simple-single-linked-lists.md) and assumed you are already familiar with arrays and vectors we can move to the next _linear data structure_ in the list of basic structures that we should know, the amazing [hash tables](https://en.wikipedia.org/wiki/Hash_table).

At simple sight a hash table is very similar to the [bucket sorting](https://en.wikipedia.org/wiki/Hash_table) we already used, we have a linear structure divided in buckets and basically when we need to _add_ a new element we calculate its key using a formula/function based in the value we need to store. This will make the whole process a $\mathcal{O}(1)$ operation for adding and searching the value _most of the times_ and that makes them a fantastic data structure for searching data that is constantly accessed (and avoiding linear or binary search).

# The hash function

We can represent a hash table with a simple array of length $n$, and use a simple formula $k = n \mod l$ to calculate the place in the array ($k$) of length $l$. In reality hash functions are a lot more complex than this and calculate an effective hash is not an easy task. If you had used or coded in .Net or Java before, you are probably aware that every object has a _hash_ function of itself (`GetHashCode` and `hashCode` in .Net and Java), this is to know what would be the correct hash code to place the element in a hash table. With this simple formula placing the value $12$ in a hash table with an internal length of $7$ would be in the index $5 \equiv 12 \pmod 7$. We know if we need to look for the value again we just calculate the hash and check if it is in that "bucket".

But what would happen if there is already another value in the same bucket? for example, 19 and 12 have the same modulo ($19 \pmod 7 \equiv 12 \pmod 7$)? This will lead to what we call _a collision_ and we have to option to _resolve_ such collision. There are many ways to do this and the easiest is simply not solving it and failing if there is an element in the hash table already.

To simplify the development, we can create a base class for hash tables and implement the "no collision" hash table:

```kotlin
abstract class Hash() {
    protected open var buckets: Array<Int?> = arrayOfNulls(7)
    protected open fun hash(value: Int): Int = value % buckets.size

    abstract fun add(value: Int)

    open fun exists(value: Int): Boolean {
        val key = hash(value)
        return buckets[key] == value
    }

    val size: Int
        get() = buckets.size
}
```

Because we don't allow collisions, we simply throw an exception:

```kotlin
class HashCollisionException(message: String): Exception(message)

/**
 * A hash table that once is a collision it throws an exception
 */
class CollisionHash(size: Int = 7): Hash() {
    override fun add(value: Int) {
        val key = hash(value)
        if (buckets[key] != null && buckets[key] != value)
            throw HashCollisionException("The value $value produces a collision in the hash")
        buckets[key] = value
    }
}
```

Simple to test as well:

```kotlin
class CollisionHashTests {
    @Test
    fun `In an empty hash nothing wrong happens`() {
        val hash = CollisionHash()
        hash.add(12)
        hash.add(2)

        assertTrue { hash.exists(12) }
        assertTrue { hash.exists(2) }
    }

    @Test
    fun `If the bucket is already occupied we throw`() {
        val hash = CollisionHash()
        hash.add(12)

        // 19 produces the same hash as 12
        assertFailsWith<HashCollisionException> { hash.add(19) }
    }

    @Test
    fun `If the bucket has already the same element nothing happens`() {
        val hash = CollisionHash()
        hash.add(12)
        hash.add(12)

        assertTrue { hash.exists(12) }
    }
}
```

While this is the easiest to implement it is as well the most unpractical to use, I mean, we will end up with a very small hash table that basically cannot keep more than just a small bunch of elements. Another collision resolution technique is _extend and rehash_ and it is pretty much as the name says, you _extend_ the inner container and then rehash all the elements and repeat until there are no collisions, this is one of the most used collision resolution in simple hash tables:

```kotlin
class ExtendHash(val growRate: Double = 1.5): Hash() {
    private fun rehash() {
        val newSize = (size * growRate).toInt()
        val items = buckets.copyOf()

        buckets = arrayOfNulls(newSize)
        for (elem in items.filterNotNull()) add(elem)
    }

    override fun add(value: Int) {
        val key = hash(value)
        if (buckets[key] != null && buckets[key] != value) {
            rehash()
            add(value)
        }
        else buckets[key] = value
    }
}
```

The tests are not really that complicated:

```kotlin
class ExtendHashTests {
    @Test
    fun `In an empty hash nothing wrong happens`() {
        val hash = CollisionHash()
        hash.add(12)
        hash.add(2)

        assertTrue { hash.exists(12) }
        assertTrue { hash.exists(2) }
    }

    @Test
    fun `If the bucket is already occupied we extend and rehash`() {
        val hash = ExtendHash()
        val initial = hash.size

        hash.add(12)
        hash.add(19)

        assertTrue { hash.exists(12) }
        assertTrue { hash.exists(19) }
        assertEquals((initial * hash.growRate).toInt(), hash.size)
    }
}
```

There is _another_ conflic resolution technique (in fact it is a whole group) named _probing_, the idea is that if the bucket is already take you search for adjacent empty buckets and place the element there. For the search process you do the same, you see if the element is in the bucket and if not you search the adjacent elements to see if it is located there. There are many different algorithms for probing, for example linear probing where we check in linear fashion until we reach the end (and shows the error) or find an available slot. I won't use much of my time writing a case around linear probing, I think you can write your own implementation with what you know now :)

A very common collision resolution algorithm is using _separate chaining_, in this idea we have a linked list in each bucket and we simply append to that linked list if we have already elements in that list. For searching we just search in that bucket linked list. This strategy won't require extending the hash but it will involve a sequential search if we have too many elements in one sole bucket.

Hash tables are pretty sweet as lookup structures, your standar library already have dictionaries or maps, those are actually hash tables, and as I explained here, creating a good hash key algorithm or placing the item in its correct bucket is not _trivial_ but it can become extremely complex. I will advice to use your existing hash structures in your library and if you have to implement your own (for some weird reason) be careful with the edge cases, pretty much the same cases as with the bucket sort algorithm.
