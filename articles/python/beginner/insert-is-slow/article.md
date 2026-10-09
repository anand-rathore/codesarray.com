title: Python list insert at the front is slow: use deque appendleft
summary: nums.insert(0, x) shifts every item in a Python list one place right, so it gets slower as the list grows. A deque adds to the front without moving anything.
description: Python list insert at the front is slow: insert(0, x) moves every item, which costs O(n). collections.deque with appendleft adds to the front in O(1).
date: 2026-10-09
read: 2 min read
follows: 5
video: insert(0, x) is slow in Python | https://youtube.com/shorts/hwHY_FSHqc8
image: cover.png
---
Adding to the front of a Python list with `nums.insert(0, x)` looks cheap, but it moves every item in the list. A `deque` from `collections` adds to the front with `appendleft` and moves nothing.

## What insert(0, x) does

```python
from collections import deque
nums = [10, 20, 30, 40]
nums.insert(0, 5)
line = deque([10, 20, 30, 40])
line.appendleft(5)
print(nums)
print(line)
```

```output
[5, 10, 20, 30, 40]
deque([5, 10, 20, 30, 40])
```

Line 3 puts `5` at the front of `nums`. To make room, Python shifts `10`, `20`, `30` and `40` one place to the right. A list is stored as an array, so a front insert costs O(n): the longer the list, the more items have to move.

## Add to the front with deque

Line 5 does the same job with `line.appendleft(5)`. A `deque` can add at either end in O(1), so nothing else moves, however long it is. Both versions print the same five numbers.

## Things to know

- `nums.insert(0, x)` is fine on a short list. The cost only matters when the list is long or you do it in a loop.
- `nums.append(x)` adds at the end and does not have this problem.
- A `deque` is built for both ends. Indexing into the middle of one is slower than on a list, so keep a list when you mostly read by position.

This is a short note on [Lists](/articles/python/beginner/lists/), lesson 5 of the Python beginner track.
