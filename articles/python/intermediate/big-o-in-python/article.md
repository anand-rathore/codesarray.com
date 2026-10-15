title: Python Big O notation: measure speed with timeit
summary: What Big O means in Python, how to measure growth with timeit at three sizes, the five curves you meet most, and what list, dict and set operations cost.
description: Python Big O notation explained: measure code with timeit at more than one size, learn O(1), O(n), O(n log n) and O(n squared), and what list, dict and set cost.
date: 2026-10-14
read: 5 min read
lesson: 1
video: Big O in Python | https://youtu.be/XbqzPFlTjQM
image: cover.png
---
By the end of this page you will be able to measure how a piece of Python code slows down as its data grows, name the five growth curves you will meet most often, and say what common list, dict and set operations cost.

## Python Big O notation: growth, not seconds

A stopwatch tells you how fast code ran on your machine today. Big O notation tells you how the time grows when the input grows. Those are different questions, and the second one is the one that decides whether a program still works when the data is a hundred times bigger.

## Measure with timeit

`timeit` from the standard library runs a small piece of code many times and returns the total seconds, so one slow moment does not fool you. A single number still says nothing about growth. Run it at ten times the size, then a hundred times, and watch what happens to the time.

## The five curves

- **O(1)**: the time stays flat, no matter how big the input.
- **O(log n)**: the time barely moves, because each step halves the work.
- **O(n)**: ten times the data, ten times the time.
- **O(n log n)**: a little worse than O(n). This is what sorting costs.
- **O(n squared)**: ten times the data, a hundred times the time. It feels fine on small test data and then collapses.

## What common operations cost

- `d[key]` and `x in some_set` are O(1).
- `nums.append(x)` is O(1) on average.
- `x in nums` on a list is O(n), because Python may check every item.
- `nums.insert(0, x)` and `nums.pop(0)` are O(n), because every other item has to shift.
- `sorted(nums)` is O(n log n).
- A loop inside a loop over the same list is O(n squared).

## The experiment

```python
from timeit import timeit

for n in (1_000, 10_000, 100_000):
    nums = list(range(n))
    seen = set(nums)
    last = n - 1
    slow = timeit(lambda: last in nums, number=1000)
    fast = timeit(lambda: last in seen, number=1000)
    print(f"{n:>7}  list {slow:.4f}s  set {fast:.4f}s")
```

The loop runs over three sizes. Each time it builds a list of that many numbers and turns it into a set. `last` is the final number, which is the worst case for the list, because the search has to look at every item before it finds it. Then `timeit` times a thousand lookups in the list and a thousand in the set, and `print` lines the results up in columns.

```output
   1000  list 0.0126s  set 0.0001s
  10000  list 0.0990s  set 0.0001s
 100000  list 1.0496s  set 0.0001s
```

The exact seconds will differ on your machine. The shape will not. The list time grows by about ten times for every ten times the data: that is O(n). The set stays at the same tiny number: that is O(1).

## What you learned

- Big O describes how time grows with the input, and `timeit` at more than one size shows it.
- O(1) stays flat, O(n) grows in step with the data, and O(n squared) is the one to avoid.
- A set or dict lookup beats a list search as soon as the data gets big.

## Common questions

**Is O(1) always faster than O(n)?** No. Big O describes growth, not speed. For a handful of items a list search can beat a set lookup. O(1) wins once the data is big enough.

**Why does the set time not change?** A set finds an item from its hash, so it does not scan the others. The cost per lookup is roughly the same whether it holds a thousand items or a hundred thousand.

**Why use the last item in the list test?** It is the worst case. `x in nums` stops at the first match, so the first item would be found at once and tell you nothing about growth.

**Why 1,000 runs per timing?** One lookup takes microseconds, which is too small and too noisy to read. A thousand runs give a total you can compare.

**Should I optimise every O(n) in my code?** No. Measure first. A single O(n) pass over a small list is fine. The ones to fix are the O(n) lookups inside loops, which turn into O(n squared).

Next: [Python iterators and generators](/articles/python/intermediate/iterators-and-generators/), and how to process a million items without holding them all in memory.
