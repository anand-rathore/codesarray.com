title: Python threads vs processes: the GIL, locks and free threading
summary: How Python threads, processes and subinterpreters differ: what the GIL is, why threads help with waiting but not calculating, how ThreadPoolExecutor and ProcessPoolExecutor compare, how a Lock stops a race condition, and what the Python 3.14 free-threaded build changes. Three short programs with their real output.
description: Python threads vs processes explained: the GIL, ThreadPoolExecutor vs ProcessPoolExecutor, threading.Lock, the 3.14 free-threaded build and InterpreterPoolExecutor, with runnable code.
date: 2026-10-24
read: 7 min read
lesson: 6
video: Python threads vs processes: the GIL and free threading | https://youtu.be/NBKUM7vekYs
image: cover.png
---
By the end of this page you will know what the Python GIL is, when threads help and when they do not, how processes get around the GIL, how to protect shared data with a lock, and what the free-threaded build and subinterpreters in Python 3.14 change. It follows [asyncio](/articles/python/advanced/asyncio/), which is the other way to overlap waiting.

## What the GIL is

CPython has a global interpreter lock, the GIL. It is one lock, and only the thread that holds it can run Python code. It exists because Python counts references to every object to know when to free it, and those counters are not safe if two threads change them at the same moment. One big lock was the simple fix.

The result: you can start four threads and still only one of them runs Python at any instant. The GIL is released when a thread waits, for the network, the disk or a sleep, and every few milliseconds it is handed to another thread.

## Threads or processes?

Ask what your program spends its time on.

- **Waiting** (websites, files, a database): use threads. A waiting thread lets go of the GIL, so the others run and the waits overlap, like asyncio but with ordinary blocking code.
- **Calculating** (loops over numbers, compressing, parsing): threads do not help, because only one can hold the GIL. Use processes. Each process is a separate Python with its own interpreter and its own GIL, so four processes really run on four cores.

The price of processes is that they do not share memory. Data you send to a process is copied across and the results are copied back, and starting a process costs more than starting a thread.

## concurrent.futures pools

You rarely build threads by hand. `concurrent.futures` gives you `ThreadPoolExecutor` and `ProcessPoolExecutor`, which have the same interface: make a pool, call `map` with a function and a list of inputs, and get the results back in order. Swap one class for the other and nothing else changes.

```python
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def count(n):
    total = 0
    for i in range(n):
        total += i
    return total

def timed(label, pool_class):
    t0 = time.perf_counter()
    with pool_class(max_workers=4) as pool:
        list(pool.map(count, [10_000_000] * 4))
    print(f"{label}: {time.perf_counter() - t0:.1f}s")

if __name__ == "__main__":
    t0 = time.perf_counter()
    for _ in range(4):
        count(10_000_000)
    print(f"one thread: {time.perf_counter() - t0:.1f}s")
    timed("4 threads", ThreadPoolExecutor)
    timed("4 processes", ProcessPoolExecutor)
```

`count` is pure calculation. `timed` runs four jobs of ten million additions in a pool of four workers. The main block times the same four jobs in one thread, then in four threads, then in four processes. On the machine used for the video it printed:

```output
one thread: 3.1s
4 threads: 3.9s
4 processes: 1.5s
```

Four threads were slower than one, because they fight over the GIL and gain nothing. Four processes were about twice as fast, not four times, because starting processes and copying data costs time. Your numbers will differ, but the order will be the same.

Two details for processes. The function and its arguments must be picklable, which means plain functions defined at the top of a module, not lambdas. And the main code must sit under `if __name__ == "__main__":`, because on Windows and macOS every worker process imports your file again.

## Race conditions and locks

Threads share memory, which is both their strength and their danger. Say four threads each add one to the same counter, a hundred thousand times. `counter += 1` looks like one step but it is three: read the value, add one, write it back. If a thread is switched out after the read and before the write, another thread can read the same old value, and one of the two updates is lost. This is a race condition. The answer comes out wrong, and differently each run, which makes it a terrible bug to find.

The fix is a lock: a `with` block that only one thread can be inside at a time.

```python
import threading

counter = 0
lock = threading.Lock()

def add(n):
    global counter
    for _ in range(n):
        with lock:
            counter += 1

threads = [threading.Thread(target=add, args=(100_000,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)
```

Line 9 takes the lock and line 10 adds one inside it. Lines 12 to 16 make four threads, start them all, and wait for each to finish with `join`. It prints:

```output
400000
```

Exactly four times a hundred thousand, on every run. Without the lock you are not promised that.

## The free-threaded build in Python 3.14

Python 3.13 added an experimental build with the GIL switched off, and Python 3.14 made it officially supported. It is installed separately, and its command is often called `python3.14t`. In it the reference counts are made safe in other ways, so threads running Python code really do run at the same time on different cores. A calculation split over four threads can then be several times faster, with no processes and no copying.

You can check which build you have with `sys._is_gil_enabled()`, which returns `False` in the free-threaded build. Three honest warnings:

- A single thread runs a little slower than in the normal build.
- Some libraries written in C have not caught up yet.
- Removing the GIL does not remove the need for locks. The counter bug above is still yours to prevent.

## Subinterpreters in Python 3.14

A subinterpreter is a second Python interpreter inside the same process, with its own state and, since Python 3.12, its own GIL. You get parallel Python code like processes, but cheaper, because it is one process. The easy way in is `InterpreterPoolExecutor`, which looks exactly like the other two pools.

```python
import sys
from concurrent.futures import InterpreterPoolExecutor

def count(n):
    return sum(range(n))

if __name__ == "__main__":
    print("GIL on:", sys._is_gil_enabled())
    with InterpreterPoolExecutor(max_workers=4) as pool:
        print(list(pool.map(count, [10, 100, 1000, 10000])))
```

```output
GIL on: True
[45, 4950, 499500, 49995000]
```

`GIL on: True` because this is the normal build; in the free-threaded build it says `False`. The interpreters do not share objects, only simple data that can be copied, so this is a safe sort of parallel: more isolated than threads, lighter than processes.

## What you learned

- The GIL lets one thread run Python at a time.
- For waiting, use threads or asyncio. For calculating, use processes, which have a GIL each but copy their data.
- `concurrent.futures` gives you thread and process pools with one interface.
- Threads share memory, so protect shared data with a `threading.Lock`.
- Python 3.14 has a free-threaded build with no GIL, and `InterpreterPoolExecutor` for subinterpreters.

## Common questions

**Is the GIL removed in Python 3.14?** Not in the normal build. Python 3.14 officially supports a separate free-threaded build with the GIL off, and the normal build keeps it. Check with `sys._is_gil_enabled()`.

**Do threads make Python faster?** For waiting on the network or disk, yes, because the waits overlap. For pure calculation, no: in the example above four threads took 3.9 seconds against 3.1 for one.

**Why do I need `if __name__ == "__main__":` with processes?** On Windows and macOS each worker process imports your file again. Without the guard, every worker would start more workers.

**Do I still need locks without the GIL?** Yes, and arguably more. A lock protects your own shared data, such as the counter, whether or not the GIL exists.

**Which should I use: threads, processes or asyncio?** Many network waits: asyncio or threads. Heavy calculation: processes, or threads on the free-threaded build. Next in the series is [the memory model and garbage collection](/articles/python/advanced/).
