title: Python asyncio: async, await, gather and timeouts explained
summary: How Python asyncio works: the event loop, async def and await, running many things at once with create_task and gather, putting a limit on the wait with timeout, keeping tasks safe with TaskGroup, why a blocking call freezes everything, and the Python 3.14 tools that show running tasks. Three short programs with their real output.
description: Python asyncio explained: the event loop, async and await, gather, timeout, TaskGroup and to_thread, plus the new 3.14 asyncio ps and pstree, with runnable code.
date: 2026-10-23
read: 9 min read
lesson: 5
video: Python asyncio: async, await, gather and timeouts | https://youtu.be/aOKr5EvYtzs
image: cover.png
---
By the end of this page you will know what the asyncio event loop does, how `async` and `await` work, how to run many waits at the same time with tasks and `asyncio.gather`, how to put a time limit on them, and how Python 3.14 lets you look inside a running program. It builds on [iterators and generators](/articles/python/intermediate/iterators-and-generators/), where a function can pause and carry on later, and on [closures and scope](/articles/python/intermediate/closures-and-scope/).

## Why asyncio: overlap the waiting

You need three pieces of data and each takes about a second to arrive. That second is not computing: it is waiting for the network to answer. If you ask for them one after another the total is three seconds, and for most of that time your program does nothing. Asyncio fixes this. While one request waits, the program starts the next, so the waits overlap and the total is about one second, the longest single wait.

Nothing got faster. It is still one thread, and one thing runs at a time. Asyncio stops you wasting the waiting time, which is why it is for input and output, waiting on the network or the disk, and not for heavy calculation.

## The event loop, `async def` and `await`

The event loop is a manager with a list of jobs. It picks a job and runs it. The job runs until it reaches a point where it has to wait, then it hands control back and the loop picks another job. When the thing a job was waiting for is ready, the loop puts that job back on the list. Jobs take turns, and they only switch at the places where they wait.

- `async def job():` makes a coroutine function. Calling `job()` does not run it: it gives you a coroutine object, a job that has not started.
- `await asyncio.sleep(1)` marks the place where a job may pause. It means: run something else, and come back to me when this is ready.
- `await` only works inside an `async def`, and a function with no `await` in it never gives the loop a chance to switch.

## Tasks and `asyncio.gather`

If you just `await` one coroutine after another you are back to waiting in a line. To start a job in the background, wrap it in a task with `asyncio.create_task(job())`. The loop begins it at the next chance, your code carries on, and later you `await task` to get its result.

For a whole group, use `asyncio.gather`. It runs the coroutines as tasks, waits for all of them and returns a list of results in the order you passed them in, not the order they finished. If one job raises an error, `gather` passes it up to you and the others keep running. Pass `return_exceptions=True` and the errors come back in the list, next to the good results.

```python
import asyncio
import time

async def fetch(name, delay):
    print(f"start {name}")
    await asyncio.sleep(delay)
    print(f"done {name}")
    return name.upper()

async def main():
    t0 = time.perf_counter()
    results = await asyncio.gather(
        fetch("a", 1),
        fetch("b", 2),
        fetch("c", 1.5),
    )
    print(results)
    print(f"took {time.perf_counter() - t0:.1f}s")

asyncio.run(main())
```

```output
start a
start b
start c
done a
done c
done b
['A', 'B', 'C']
took 2.0s
```

`fetch` is an async function: it prints, pauses at the `await`, then prints again and returns the name in capitals. `asyncio.run(main())` starts the event loop, runs `main` and closes the loop: it is the one entry point of an asyncio program. All three jobs start at once, before any is done. They finish in the order of their waits (1, 1.5 and 2 seconds), but the result list is `['A', 'B', 'C']`, the order we asked. The total is 2.0 seconds, the longest wait, not 4.5, the sum.

## Timeouts with `asyncio.timeout`

Waiting forever is a bug, so anything that talks to the network needs a time limit. Since Python 3.11 the tool is `asyncio.timeout`, used as a context manager. Everything inside the block must finish within the limit. If it does not, the work inside is cancelled and a `TimeoutError` is raised, which you catch outside the block. There is also the older `asyncio.wait_for(job(), 1)`, which does the same for a single awaitable.

## TaskGroup keeps tasks inside a block

`asyncio.TaskGroup`, also from 3.11, is the tool to reach for first today. You open it with `async with` and create tasks inside it. When the block ends it waits for every task. The point is safety: if one task fails, the group cancels all the others, so nothing is left running in the background by accident. The errors come out together as an exception group, which you catch with `except*`. With `gather`, by comparison, the other tasks quietly keep going after an error. A task group makes the lifetime of the tasks match the lifetime of the block.

```python
import asyncio

async def slow():
    await asyncio.sleep(5)
    return "finished"

async def main():
    try:
        async with asyncio.timeout(1):
            print(await slow())
    except TimeoutError:
        print("gave up after 1s")

    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(asyncio.sleep(0.1, "x"))
        t2 = tg.create_task(asyncio.sleep(0.2, "y"))
    print(t1.result(), t2.result())

asyncio.run(main())
```

```output
gave up after 1s
x y
```

`slow` needs five seconds but the block allows one, so it is cancelled after one second and the `except TimeoutError` branch prints that we gave up. Then the task group starts two tasks, one that waits 0.1 s and returns `"x"`, one that waits 0.2 s and returns `"y"`. When the block ends both are finished, and `result()` on each task gives `x y`.

## A blocking call freezes the whole loop

Remember that jobs only switch at an `await`. If one job calls a normal blocking function, such as `time.sleep(1.5)` or a slow library call, there is no `await`, so there is no switch. The whole loop freezes and every other job stops until the call returns.

The fix is to keep blocking work off the loop. `asyncio.to_thread(fn)` runs the function in a worker thread and you `await` its result, so the loop stays free and the other jobs keep their rhythm. The rule: inside async code, use the async version of every wait, and if the only version is a blocking one, send it to a thread.

```python
import asyncio
import time

async def heartbeat():
    for _ in range(3):
        print("beat")
        await asyncio.sleep(0.5)

def slow_io():
    time.sleep(1.5)
    return "io done"

async def main():
    beat = asyncio.create_task(heartbeat())
    print(await asyncio.to_thread(slow_io))
    await beat

asyncio.run(main())
```

```output
beat
beat
beat
io done
```

The heartbeat prints `beat` three times, half a second apart, while `slow_io` blocks a worker thread for 1.5 seconds. If `slow_io()` were called directly instead of through `to_thread`, the heartbeat would print nothing for 1.5 seconds, because the loop would be frozen.

## New in Python 3.14: look inside a running program

Before 3.14, finding out why an async program was stuck meant guessing. Now you can ask it.

- `python -m asyncio ps PID` prints a table of every task that is waiting, with its name and what it is waiting on.
- `python -m asyncio pstree PID` prints the same as a tree, which shows which task started which. It reports a cycle of tasks waiting on each other, a deadlock.
- Inside your own code, `asyncio.print_call_graph()` prints the chain of awaits that led to the current line.

For a program with a task group of two `fetch` tasks sleeping, `pstree` shows `Task-1` awaiting `main`, then the task group, then `fetch-a` and `fetch-b`, each waiting in `sleep`. (On Windows, set `PYTHONIOENCODING=utf-8` if the tree characters raise an encoding error.)

## What you learned

- Asyncio overlaps waiting: one thread, an event loop, and jobs that take turns at each `await`.
- `async def` makes a coroutine, and `await` is where it may pause.
- `create_task` starts one in the background, and `gather` runs many and returns results in order.
- `asyncio.timeout` puts a limit on a block, and `TaskGroup` keeps tasks inside a block and cancels the rest if one fails.
- A blocking call freezes the loop: use `asyncio.to_thread`.
- In Python 3.14, `python -m asyncio ps` and `pstree` show the running tasks.

## Common questions

**Does asyncio make my code faster?** Only when it spends its time waiting, on the network or the disk. It runs one thing at a time on one thread, so it does not speed up heavy calculation.

**What is the difference between a coroutine and a task?** Calling an `async def` function gives a coroutine that has not started. `asyncio.create_task` wraps it in a task that the event loop starts running in the background.

**Why are `gather` results in a different order from the output?** `gather` returns results in the order you passed the coroutines, not the order they finished. In the example the prints show `a`, `c`, `b` but the list is `['A', 'B', 'C']`.

**Should I use `gather` or `TaskGroup`?** Prefer `TaskGroup` for new code: if one task fails it cancels the rest and raises an exception group. With `gather`, the other tasks keep running after an error unless you cancel them yourself.

**Why did my whole program freeze inside an `async def`?** Something blocking, such as `time.sleep` or a synchronous library call, ran without an `await`. Replace it with an async version, or run it with `asyncio.to_thread`.

**Can I use `await` outside an `async def`?** No. Start the program with `asyncio.run(main())` and put the awaits inside `async def` functions.

Next in the series: threads, processes and free threading.
