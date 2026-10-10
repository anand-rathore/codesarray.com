title: Python functions: def, return, default arguments and *args
summary: Write your own Python functions with def, return a result, use default and keyword arguments, understand local variables, and collect any number of arguments with *args.
description: Python functions for beginners: define one with def, return a value, use default and keyword arguments, local scope, *args and **kwargs.
date: 2026-10-10
read: 4 min read
lesson: 8
video: Functions | https://youtu.be/iDfj4jORrRQ
image: cover.png
---
A Python function is a named block of code you can run again and again. By the end of this page you will write your own with `def`, return a result with `return`, give parameters default values, pass arguments by name, know why a variable made inside a function stays inside it, and collect any number of arguments with `*args`.

## def, call and return

You write `def`, a name, brackets and a colon. The indented lines are the body. `def area(width, height=1):` starts a function called `area`. Calling it, `area(3, 4)`, runs the body with `width` as `3` and `height` as `4`. The `return` line hands the result back, so you can print it or store it. A function with no `return` gives back `None`.

## Parameters and defaults

Parameters are the names in the brackets. A default, like `height=1`, is used when you leave that argument out, so `area(5)` uses a height of `1` and gives `5`. You can also pass arguments by name: `area(height=2, width=6)`. Names make a call easy to read, and the order stops mattering.

## Local variables

A variable made inside a function is local. In `greet`, `message` exists only while the function runs. Using `message` after the call raises `NameError: name 'message' is not defined`. A function sends values out through `return`, not by leaking names.

## *args and **kwargs

Sometimes you do not know how many arguments will come. A star before a name, `*nums`, collects them all into a tuple. `total(1, 2, 3)` puts `(1, 2, 3)` into `nums`, and `sum(nums)` adds them up. A double star, `**kwargs`, does the same for named arguments, collecting them into a dictionary.

```python
def area(width, height=1):
    """Return width times height."""
    return width * height

print(area(3, 4))
print(area(5))
print(area(height=2, width=6))

def total(*nums):
    return sum(nums)

print(total(1, 2, 3))

def greet(name):
    message = "Hi " + name
    return message

print(greet("Ada"))
```

```output
12
5
12
6
Hi Ada
```

Line 1 defines `area` with a default height of `1`. Line 2 is the docstring, a sentence saying what the function does. Line 3 returns `width * height`. Line 5 calls it with `3` and `4` and prints `12`. Line 6 leaves out the height, so it prints `5`. Line 7 passes both by name and prints `12`. Line 9 defines `total` with `*nums`, line 10 returns the sum, and line 12 prints `6`. Lines 14 to 16 define `greet`, which builds a local `message` and returns it, so line 18 prints `Hi Ada`.

## What you learned

- `def` defines a function, and `return` sends a value back; with no `return` you get `None`.
- A default value fills in an argument you leave out, and you can pass arguments by name.
- Variables made inside a function are local to it.
- `*args` collects any number of arguments into a tuple, and `**kwargs` collects named ones into a dictionary.
- A docstring on the first line of the body says what the function does.

## Common questions

**What is the difference between a parameter and an argument?** A parameter is the name in the definition, like `width`. An argument is the value you pass when you call it, like `3`.

**Does `print` return a value?** No. `print` shows text and returns `None`. If you want a result you can reuse, `return` it instead of printing it.

**Can a function return more than one value?** Yes. `return 1, 2` returns a tuple, and you can unpack it: `a, b = f()`.

**Can a default come before a parameter without one?** No. `def area(height=1, width)` is a `SyntaxError`. Put parameters without defaults first.

**What do the names `args` and `kwargs` mean?** They are only a habit. The stars do the work, so `*nums` behaves the same as `*args`.

This lesson follows on from [Python dictionaries](/articles/python/beginner/dictionaries/). Next in the series: comprehensions.
