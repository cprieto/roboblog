---
title: queues with Python asyncio
date: 2021-07-06
slug: queues-with-python-asyncio
tags: python, asyncio, asynchronous programming
twitter_image: async_queue.jpg
---

I really love asynchronous programming, and the support for asynchronous programming structures out there in modern languages is amazing (even C++20 has coroutines now!), though I personally think the biggest problem with _async_ programming is that is so easy to use (thanks to the support I mentioned before) and you tend to believe you are an expert on it and just sprinkle it over everywhere without fully understand how it works and what is going to happen, this is specially problematic with [event loop](https://en.wikipedia.org/wiki/Event_loop) based approaches (like the one by default in Python).

I like to think that when you learn a language, more than just learning the _keywords_ and _constructs_ of the language, you should put effort and energy in understanding _the idea_ behind the language, why is there? what is trying to solve? and maybe you won't use the language in production but if you take the time to understand the [language paradigm](https://en.wikipedia.org/wiki/Programming_paradigm) I am pretty sure you will get ideas and constructs that you can easily adapt or learn faster in your day to day programming language.

A few years ago I started using [Python asyncio](https://docs.python.org/3/library/asyncio.html), and a very common problem appeared, especially when you create a lot of _background coroutines_:

 > How to communicate between working coroutines _in an effective way_

A good example of this is the following problem

```text
coroutine 1:
    produces data

coroutine 2:
    consumes data from coroutine 1
    only when there is data available
```

Gladly I had seen this problem so many times before in Go, a problem that is easily solved using [Go channels](https://tour.golang.org/concurrency/2) but, of course, Python does not have channels... But it has a nice structure, _the [Queue]()_!

```python
import asyncio

async def producer(channel: asyncio.Queue):
    for num in range(0, 5):
        await asyncio.sleep(1)
        await channel.put(num)

async def consumer(channel: asyncio.Queue):
    while True:
        item = await channel.get()
        print(f'Got number {item}')

async def main():
    channel = asyncio.Queue()
    cons = asyncio.create_task(consumer(channel))

    # When no producer finished we are done
    await producer(channel)
    print('Done!')

asyncio.run(main())
```

In this example, `asyncio.Queue` is our way to communicate between the producer of items and it consumer, it will _await_ until the _channel_ (our queue) has an item to give us and it is controlled by the loop mechanism used in asyncio, it is not as powerful as a channel but it does the job. Notice many coroutines can be producing items to the channel, it is easy to modify the previous example to see it in action:

```python
async def main():
    channel = asyncio.Queue()
    cons = asyncio.create_task(consumer(channel))

    # Wait for all producers to finish
    await asyncio.wait({
        asyncio.create_task(producer(channel, 0)),
        asyncio.create_task(producer(channel, 10))
    })
    print('Done!')
```

The queue in Python is a very powerful structure and there are different implementations depending on your model, for example `queue.Queue` for threading applications and `multiprocessing.Queue` for applications using the multiple process model.

Lesson learned: Sometimes you can use the knowledge learned in one language to solve a problem using a similar way in another language.