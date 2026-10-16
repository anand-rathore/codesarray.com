title: Python stacks and queues: list, deque and why pop(0) is slow
summary: What a stack and a queue are, how to build a stack from a list and a queue from a deque, and why pop(0) on a list costs O(n) while popleft on a deque does not.
description: Python stacks and queues explained: use a list as a stack, a deque as a queue, and see why pop(0) is O(n) while popleft is O(1).
date: 2026-10-16
read: 4 min read
lesson: 7
video: Python Stacks and Queues Explained | https://youtu.be/ZfKK3-NgLQk
image: cover.png
---
By the end of this page you will know what a stack is, what a queue is, and why a `deque` is the right tool for a queue. It builds on [Python type hints](/articles/python/intermediate/type-hints/) and [Big O in Python](/articles/python/intermediate/big-o-in-python/).

## What is a stack in Python

A stack is last in, first out. Think of a pile of plates: you put a plate on top, and you take a plate from the top. In Python, a list works as a stack. `append` adds to the end and `pop` takes from the end. Both are fast.

Here is the whole example. It is used for every section below.

```python
from collections import deque

stack = []
stack.append("a")
stack.append("b")
print(stack.pop())

queue = deque()
queue.append("a")
queue.append("b")
print(queue.popleft())
```

```output
b
a
```

## What is a queue in Python

A queue is first in, first out. Think of a line at a shop: the first person to join is the first person served. You add at the back and you take from the front.

## Why use a deque, not a list

A list can act as a queue, but it is slow. `pop(0)` takes the first item, and then every other item has to shift one place left. That costs O(n). A `deque`, from the `collections` module, is built for both ends. Its `popleft()` is O(1).

## The stack and queue example, line by line

Line 1 imports `deque`. Line 3 makes an empty list, our stack. Lines 4 and 5 append `"a"` and `"b"`. Line 6 pops, and the last one in comes out first, so it prints `b`. Line 8 makes a `deque`, our queue. Lines 9 and 10 append `"a"` and `"b"`. Line 11 calls `popleft()`, and the first one in comes out first, so it prints `a`.

## What you learned

- A stack is last in, first out. A list does it with `append` and `pop`.
- A queue is first in, first out.
- A `deque` gives a fast `popleft()`, where a list needs a slow `pop(0)`.

## Common questions

**Can I use a list as a queue?** Yes, but `pop(0)` shifts every remaining item, so it costs O(n). For a long queue, use a `deque`.

**Is `deque.append` fast too?** Yes. `append` and `popleft` are both O(1), and so are `appendleft` and `pop`.

**Is there a built-in stack type?** No. A list is the usual stack. `append` pushes and `pop` pops, both at the end.

**What does `queue.Queue` do?** It is a queue built for threads, with locking. For ordinary single-threaded code, a `deque` is simpler and faster.

Next in the series: linked lists, and how to build one from classes.
