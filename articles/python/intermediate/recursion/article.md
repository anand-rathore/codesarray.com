title: Python recursion explained: call stack and base case
summary: How recursion works in Python: a function that calls itself on a smaller problem, the call stack that holds the waiting calls, the base case that stops them, and the RecursionError you get without one.
description: Python recursion explained: write a factorial function, see how calls pile up on the call stack, and why a base case stops a RecursionError.
date: 2026-10-17
read: 4 min read
lesson: 9
video: Python Recursion Explained | https://youtu.be/EaIIsJr_-0I
image: cover.png
---
By the end of this page you will be able to write a recursive function in Python, explain how the call stack keeps track of the calls, and say why every recursive function needs a base case. It builds on [Python closures and scope](/articles/python/intermediate/closures-and-scope/), since each call gets its own local variables.

## What is recursion in Python

Recursion is a function that calls itself with a smaller problem. Each call solves a little of the job and hands the rest to the next call. A classic example is factorial: 4 factorial is 4 times 3 factorial, and 3 factorial is 3 times 2 factorial, and so on down to 0 factorial, which is 1.

Here is the whole example. It is used for every section below.

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


# try it
print(factorial(4))
print(factorial(0))
```

```output
24
1
```

## The call stack

When `factorial(3)` calls `factorial(2)`, the first call cannot finish yet. It has to wait for the answer. Python keeps these waiting calls in a pile called the call stack. Each new call goes on top of the pile, so `factorial(3)`, `factorial(2)` and `factorial(1)` stack up, newest on top.

The call on top is the only one running. The ones below it are waiting.

## The base case

The pile has to stop growing. The base case is the one input the function answers without calling itself. Here it is lines 2 and 3: when `n` is 0, return 1.

Once the base case answers, the calls finish one by one from the top down. Each waiting call takes the answer, multiplies it, and returns. For `factorial(3)` that is 1 times 1, then 2 times 1, then 3 times 2, and the answer is 6.

## Without a base case: RecursionError

Remove the base case and the function calls itself forever. The pile keeps growing, so Python stops it. At about 1000 calls it raises a `RecursionError`:

```output
RecursionError: maximum recursion depth exceeded
```

So the base case is not optional, and every call must move closer to it. Here `n - 1` moves toward 0.

## The recursive example line by line

- Line 1 defines `factorial` with a number `n`.
- Line 2 checks the base case, `n == 0`.
- Line 3 returns 1 without calling again.
- Line 4 is the recursive step: `n * factorial(n - 1)`.
- Line 8 prints `factorial(4)`, which is 24.
- Line 9 prints `factorial(0)`, which hits the base case straight away and gives 1.

## What you learned

- Recursion is a function calling itself on a smaller problem.
- Waiting calls pile up on the call stack.
- A base case stops the pile, and the calls then finish from the top down.
- Without a base case, Python raises `RecursionError` after about 1000 calls.

## Common questions

**What is the recursion limit in Python?** The default is about 1000 calls deep. You can read it with `sys.getrecursionlimit()`. Raising it is rarely the right fix: a function that needs thousands of levels is usually better written as a loop.

**Is recursion faster than a loop?** No. In Python a loop is usually a little faster and uses less memory, because each recursive call adds a stack entry. Recursion is worth it when the problem is naturally nested, as in trees.

**Why does factorial of 0 equal 1?** It is a definition that makes the pattern work: 1 factorial is 1 times 0 factorial, so 0 factorial has to be 1.

**Can a recursive function call itself more than once?** Yes. Fibonacci calls itself twice per call, which repeats a lot of work. Caching the results with `functools.lru_cache` fixes that, and a later lesson shows how.

**What happens with a negative number?** `factorial(-1)` never reaches 0, because `n - 1` moves away from it, so it ends in a `RecursionError`. A real function would check for that first.

Next in the series: binary search, and how to find an item by halving the problem.
