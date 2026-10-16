title: Python decorators explained: @wraps, arguments and lru_cache
summary: What the at sign above a function really does, how to write a decorator, how functools.wraps keeps the name, how to give a decorator arguments, and how lru_cache makes recursive Fibonacci instant.
description: Python decorators explained: how a wrapper function works, what @ really does, functools.wraps, decorators with arguments, and lru_cache for free caching.
date: 2026-10-16
read: 5 min read
lesson: 4
video: Python Decorators Explained | https://youtu.be/7EVB3A3ktmY
image: cover.png
---
By the end of this page you will know what the `@` above a Python function really does, be able to write your own decorator that logs a call, and know how a single line of `functools.lru_cache` turns slow recursive Fibonacci into an instant one.

## Python decorators: a function that wraps a function

In Python a function is a value, so you can pass it to another function. A decorator is a function that takes a function, builds a wrapper around it, and returns the wrapper. The wrapper runs some code before, calls the original, and runs some code after. The original function is never changed.

```python
import functools

def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"returned {result}")
        return result
    return wrapper

@logged
def add(a, b):
    return a + b

add(2, 3)
```

```output
calling add(2, 3)
returned 5
```

## What the @ sign really does

The at sign is shorthand. Writing `@logged` above `def add` means exactly `add = logged(add)`, run right after the function is defined. From then on the name `add` points at the wrapper, so every call goes through it first. That is why a decorator can log a call, time it, or check its arguments.

## functools.wraps keeps the name

The wrapper replaces the original, so the original's details are lost. Without `functools.wraps`, a decorated `add` reports `add.__name__` as `'wrapper'` and its docstring is `None`. Putting `@functools.wraps(func)` on the wrapper copies the name and docstring across, so tracebacks, `help()` and debugging still show the real function. It also sets `add.__wrapped__` to the original.

## Decorators with arguments

What if the decorator needs a setting, such as repeating a call three times? Add one more layer. The outer function takes the setting and returns the decorator. The decorator takes the function and returns the wrapper.

```python
import functools

def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def hi():
    print("hi")

hi()
```

```output
hi
hi
hi
```

So `@repeat(3)` calls `repeat(3)` first, and the decorator it returns is what gets applied to `hi`.

## lru_cache: a decorator you do not have to write

The standard library ships with useful decorators. `@functools.lru_cache` remembers the result for each set of arguments. Recursive Fibonacci of 30 makes 2,692,537 calls without it, and 31 with it:

```python
import functools

@functools.lru_cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30))
print(fib.cache_info())
```

```output
832040
CacheInfo(hits=28, misses=31, maxsize=128, currsize=31)
```

Each value is computed once (31 misses) and every repeat is a lookup (28 hits). Same code, one line added.

## The logging decorator, line by line

The first snippet is the whole walkthrough. `logged` takes `func`. `@functools.wraps(func)` keeps the name. `wrapper` accepts any arguments with `*args` and `**kwargs`, prints the call, calls the original and keeps the result, prints it, and returns it so callers still get their answer. The last line of `logged` returns `wrapper` without calling it. `@logged` applies it to `add`, and `add(2, 3)` prints the two lines above.

## What you learned

- A decorator is a function that takes a function and returns a wrapper.
- `@name` above a function is shorthand for `f = name(f)`.
- Add `functools.wraps` to keep the name and docstring.
- A decorator with arguments is one extra layer: a function that returns the decorator.
- `functools.lru_cache` gives you memoisation for free.

## Common questions

**Should the wrapper always return the result?** Yes, unless you mean to throw it away. If the wrapper forgets `return result`, the decorated function silently returns `None`.

**Why `*args, **kwargs` in the wrapper?** So the wrapper accepts whatever the original accepts and passes it all on. Without them the decorator only works for one signature.

**Can I stack decorators?** Yes. The one closest to `def` is applied first. `@a` above `@b` above `def f` means `f = a(b(f))`.

**What is the difference between `lru_cache` and `functools.cache`?** `lru_cache` keeps at most 128 results by default and drops the least recently used. `functools.cache` has no limit. Both need arguments that are hashable, so passing a list raises `TypeError: unhashable type: 'list'`.

**How do I clear a cache?** Call `fib.cache_clear()`. It resets the hits, misses and size shown by `cache_info()`.

Next in the series: object oriented Python, and the special methods behind every class.
