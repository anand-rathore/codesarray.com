title: Python heapq: heaps and priority queues explained
summary: How a Python heap always gives you the smallest item first. The heap rule, pop and push at O(log n), heapq on a plain list, and a tiny task scheduler with its real output.
description: Python heapq explained: how a heap keeps the smallest item on top, how heappush and heappop work, and how to build a priority queue, with real output.
date: 2026-10-18
read: 4 min read
lesson: 13
video: Python Heaps and Priority Queues with heapq | https://youtu.be/GnawBXFH-nw
image: cover.png
---
By the end of this page you will know how to always get the smallest item first in Python, without sorting the whole list, using a heap and the `heapq` module. It builds on [Python hash tables](/articles/python/intermediate/hash-tables/), another structure that finds things fast.

## What is a heap in Python

A heap is a tree where every parent is smaller than its children. So the smallest item always sits at the top, called the root. Take the numbers 5, 1, 4, 3. As a heap, 1 is the root, 3 and 4 hang below it, and 5 hangs below 3.

Only the top is guaranteed. The rest is not fully sorted, and that is fine: a heap does less work than a sorted list because it only promises the smallest item. A heap used this way, to serve items by priority, is called a priority queue.

## Pop and push

Taking the smallest item is called a pop. Python removes the root, 1. Then it moves the last item, 5, up to the top and lets it sink: it swaps with the smaller child, 3, until both its children are bigger. Now 3 is the new top.

A push works the other way. The new item goes in at the bottom and floats up while it is smaller than its parent. A tree of a million items is only about 20 levels deep, so both push and pop take O(log n).

## heapq: a heap in a plain list

Python has no separate heap type. The `heapq` module keeps a heap inside an ordinary list. The smallest item is always at index 0, so you can look at it without removing it: `h[0]`. You add with `heapq.heappush(h, item)` and remove the smallest with `heapq.heappop(h)`.

To order things by priority, push tuples. Python compares tuples from the first item, so the first number is the priority.

```python
import heapq

tasks = []
heapq.heappush(tasks, (3, "email"))
heapq.heappush(tasks, (1, "fix bug"))
heapq.heappush(tasks, (2, "lunch"))

while tasks:
    priority, name = heapq.heappop(tasks)
    print(priority, name)
```

```output
1 fix bug
2 lunch
3 email
```

We pushed `email` first, but the tasks come out by priority.

## The code line by line

- Line 1 imports `heapq`.
- Line 3 makes an empty list, which will hold the heap.
- Lines 4 to 6 push three tasks. Each is a tuple of a priority and a name.
- Line 8 loops while the list is not empty, so we never pop from an empty heap.
- Line 9 pops the smallest task and unpacks it into `priority` and `name`.
- Line 10 prints it.

## What you learned

- A heap keeps the smallest item on top; the rest is not fully sorted.
- Push and pop cost O(log n), and peeking at `h[0]` is free.
- `heapq` turns a plain list into a priority queue, and tuples set the priority.

## Common questions

**Does `heapq` give a max heap?** No, it is always a min heap. For the largest item first, push the negative of each number and negate it again after the pop: pushing -5, -1, -4, -3 and popping gives -5, which is 5.

**Is the list sorted after I push items?** No. Pushing 5, 1, 4, 3 one by one leaves the list as `[1, 3, 4, 5]`, which happens to look sorted, but after one pop it is `[3, 5, 4]`. Only index 0 is guaranteed. Use `sorted()` when you need the whole order.

**What happens if I pop from an empty heap?** Python raises `IndexError: index out of range`. That is why the loop above checks `while tasks`.

**How do I turn an existing list into a heap?** Call `heapq.heapify(x)`. It rearranges the list in place in O(n), which is faster than pushing the items one at a time.

**How do I get the largest or smallest few items?** `heapq.nlargest(2, [5, 1, 4, 3])` returns `[5, 4]`, and `heapq.nsmallest(2, [5, 1, 4, 3])` returns `[1, 3]`.

Next in the series: trees and traversal, and how to visit every node.
