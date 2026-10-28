title: Python profiling and performance: cProfile, timeit and NumPy
summary: How to profile Python code and make it faster: time small pieces with timeit, find the slow function with cProfile, read tottime and cumtime, fix the data structure first, use NumPy vectorisation, and what the sampling profiler in Python 3.15 and the experimental JIT in 3.14 change. Three short programs with their real output.
description: Python profiling and performance: timeit, cProfile, tottime vs cumtime, data structures, NumPy vectorisation, the 3.15 sampling profiler and the 3.14 JIT, with real output.
date: 2026-10-28
read: 10 min read
lesson: 10
video: Python profiling and performance | https://youtu.be/N79j7oO-pjc
image: cover.png
---
By the end of this page you will know how to find out why Python code is slow, and what to do about it: how to time a small piece of code with `timeit`, how to find the slow function in a real program with `cProfile`, why the biggest wins are usually a better data structure and not a clever trick, how NumPy makes numeric loops fast, and what the sampling profiler coming in Python 3.15 and the experimental JIT in Python 3.14 do and do not promise. The rule for all of it is one word: measure. It follows [the Python import system](/articles/python/advanced/import-system/).

## Time small code with timeit

`timeit` runs a statement many times and tells you how long that took. You give it the statement, a setup string that runs once and is not timed, and `number`, how many times to run the statement. One run of a fast line is too short to measure, so you repeat it a thousand times. Then you repeat the whole measurement a few times with `repeat` and keep the smallest result. Noise from your computer can only add time, never remove it, so the minimum is the cleanest number. `timeit` also switches the garbage collector off while it times, so a collection does not land in the middle of your numbers.

```python
from timeit import repeat

setup = "items = list(range(10_000))"
best = min(repeat("9_999 in items", setup, number=1_000, repeat=3))
print(f"list {best * 1000:.2f} ms")
setup = "items = set(range(10_000))"
best = min(repeat("9_999 in items", setup, number=1_000, repeat=3))
print(f"set  {best * 1000:.2f} ms")
```

The statement asks for the last item on purpose: the worst case for a list, which walks the whole list from the start.

```output
list 69.80 ms
set  0.04 ms
```

A thousand searches took about seventy milliseconds on a list and four hundredths of a millisecond on a set: more than a thousand times faster, from one change of data structure. Your numbers will differ, but the gap will be this big. Time one idea at a time, and always compare, because a single time on its own tells you little.

## Find the slow function with cProfile

`timeit` answers which of two things is faster. A profiler answers a different question: in my whole program, where does the time go? Python ships one, `cProfile`. It watches every function call, and for each function it records:

- `ncalls`: how many times it was called.
- `tottime`: the time spent inside the function's own lines, not counting the functions it called.
- `cumtime`: the time including everything it called.

So `main` has a huge `cumtime`, because it calls everything, and a tiny `tottime`. The function with the biggest `tottime` is where the work really happens, and that is the one to read first. You can profile a whole script from the command line with `python -m cProfile -s tottime script.py`, or profile a block of code with a `with` statement, as the program below does. One cost: `cProfile` hooks every single call, so the program runs noticeably slower while profiled. Trust the proportions, not the exact seconds.

```python
import cProfile
import pstats


def with_list(n):
    seen = []
    for i in range(n):
        if i not in seen:
            seen.append(i)
    return len(seen)


def with_set(n):
    seen = set()
    for i in range(n):
        seen.add(i)
    return len(seen)


def main():
    with_list(5_000)
    with_set(5_000)


with cProfile.Profile() as pr:
    main()
stats = pstats.Stats(pr).get_stats_profile()
rows = sorted(stats.func_profiles.items(), key=lambda kv: kv[1].tottime, reverse=True)
for name, f in rows[:3]:
    print(f"{f.tottime:.3f}s {f.ncalls:>5} calls  {name}")
```

`with_list` and `with_set` do the same job: build a list of unique numbers. Line 25 starts the profiler as a context manager and runs `main` inside it. Lines 27 and 28 turn the recorded data into statistics and sort the functions by total time, biggest first. The loop prints the top three.

```output
0.096s     1 calls  with_list
0.001s     1 calls  with_set
0.001s  5000 calls  <method 'append' of 'list' objects>
```

At the top is `with_list`: one call, about a tenth of a second, almost the whole run. Notice something important: the check `i not in seen` is not a function, so the profiler does not list it. Its time is counted inside `with_list`'s own `tottime`. The profile tells you which function to look into, and then you read its lines to find the cause. Here it is `not in` on a list, and the fix is the one from before: use a set.

## The sampling profiler in Python 3.15

There is another way to profile, and it is coming to the standard library in Python 3.15: a sampling profiler. Instead of hooking every call, it looks at what the program is doing many times every second and writes down the function it caught. After a few thousand looks, the functions where the program spends time show up most often. Because it does not touch every call, the overhead is small and the program runs at nearly its normal speed. It can also attach to a program that is already running, given its process ID, with nothing restarted, which is what you want for a server that is slow in production.

```bash
python -m profiling.sampling run script.py
python -m profiling.sampling attach 12345
```

It can print a table or write a flame graph, an interactive picture where the widest bar is the most expensive function. This is new in Python 3.15, which is coming, so you cannot run it on 3.14. `cProfile` stays the tool for today.

## Make it faster: data structures first

Once you know where the time goes, ask one question before any trick: is it the algorithm or the data structure? That is where the big wins live. Checking whether a number is in a list walks the list from the start, so it is O(n). Checking a set is a hash lookup, O(1). With ten thousand items that single change is more than a thousand times faster, and no amount of micro tuning beats it. After that:

- Let built-in functions do the loop. `sum`, `min`, `sorted` and the string methods are written in C, and a loop in C is much faster than the same loop written in Python.
- Do not repeat work. A value computed inside a loop that never changes belongs above the loop, and a function called again and again with the same arguments can use `functools.lru_cache`, which the [dynamic programming article](/articles/python/advanced/dynamic-programming/) covers.
- Fix the top of the table first. If the profile says a function takes two percent of the time, making it twice as fast saves one percent.

## NumPy vectorisation

Sometimes the loop itself is the problem: millions of numbers, one Python operation each. Every pass of a Python loop has to look at the object, check its type and create a new object for the result. NumPy avoids that. A NumPy array stores plain numbers side by side in memory, all of one type, and an operation like `arr * arr` runs one fast loop in C over the whole array. That style is called vectorisation: you write the operation once, for the whole array, with no `for` loop at all. If you can describe the work as the same operation on every item, ask whether NumPy has it. NumPy is not in the standard library; install it with `uv add numpy`.

```python
import numpy as np
from timeit import timeit

nums = list(range(1_000_000))
arr = np.arange(1_000_000)

print(sum(x * x for x in nums) == int((arr * arr).sum()))
print(f"loop  {timeit(lambda: sum(x * x for x in nums), number=5):.2f} s")
print(f"numpy {timeit(lambda: (arr * arr).sum(), number=5):.2f} s")
```

Line 7 checks that both ways give the same sum of squares, because a fast wrong answer is no use. The Python way is a generator with `sum`; the NumPy way is `arr * arr` and then `.sum()`.

```output
True
loop  0.43 s
numpy 0.01 s
```

Both give the same answer. The Python loop takes about four tenths of a second for five runs; the NumPy version takes about one hundredth. That is dozens of times faster, with less code. The pattern is: let the profiler find the hot spot, pick a better data structure or a vectorised operation, then time it again to prove the change worked. The cost is moving data in and out of an array, so for ten items it is not worth it, but for a million it is a very different speed.

## The JIT in Python 3.14

A just-in-time compiler turns hot code, code that runs many times, into machine code while the program runs. CPython has had an experimental one since Python 3.13, and the official Windows and macOS builds of 3.14 include it. It is off by default. You turn it on by setting the environment variable `PYTHON_JIT=1` before you start Python. What it does today: the speed-up is small, it is uneven from one program to another, and some programs get no faster at all. It is not a fix for slow code and no reason to skip the steps above. Measure your own program with and without it, and keep it only if the numbers say so.

## What you learned

- Do not guess, measure.
- `timeit` compares small pieces of code: use `repeat` and keep the smallest time.
- `cProfile` shows where a whole program spends time: read `tottime` first, and remember that `cumtime` includes the functions it calls.
- The sampling profiler, coming in Python 3.15, does the same with low overhead and can attach to a running program.
- Fix the algorithm and the data structure before any trick.
- Let NumPy loop for numbers.
- The JIT in Python 3.14 is experimental and off by default; keep it only if you measure a gain.

## Common questions

**Why keep the minimum from `repeat` and not the average?** Because anything else running on your computer can only make a run slower, never faster, so the smallest time is the one least disturbed by noise.

**What is the difference between `tottime` and `cumtime`?** `tottime` is the time inside a function's own lines. `cumtime` also counts every function it called. A function that only calls others has a large `cumtime` and a small `tottime`.

**Why does the profile not show my `in` check on a list?** `i not in seen` is an operator, not a function call, so the profiler does not list it. Its time is counted in the `tottime` of the function that contains the line, here `with_list`.

**Does profiling slow my program down?** Yes. `cProfile` hooks every function call, so the program runs slower while profiled. The proportions between functions are what to trust, not the exact seconds.

**Is the sampling profiler available now?** Not yet: `profiling.sampling` is coming in Python 3.15. On 3.14, use `cProfile`.

**Should I turn the JIT on?** Only if you measure a gain. In Python 3.14 it is experimental and off by default, set with `PYTHON_JIT=1`, and the speed-up is small and uneven.

Next in the series is design patterns.
