title: Python type hints explained: str, list[int] and int | None
summary: How to add type hints to a Python function, describe a list with list[int], mark a value that might be None with int | None, and what a type checker does with the hints.
description: Python type hints explained: annotate parameters and return values, use list[int] and int | None, and see what a type checker like mypy catches before you run.
date: 2026-10-16
read: 4 min read
lesson: 6
video: Python Type Hints Explained | https://youtu.be/LJoQW2Yas6E
image: cover.png
---
By the end of this page you will know how to annotate a function with type hints, how to describe what a list holds, how to say a value might be `None`, and what a type checker does with all of it. It builds on [Python classes](/articles/python/intermediate/oop-deep-dive/) and the [functions lesson](/articles/python/beginner/functions/).

## Python type hints on a function

A type hint is a label on a name. After a parameter, write a colon and a type, like `name: str`. After the closing bracket, write an arrow and the return type, like `-> str`. The hints are notes for people and tools. Python itself does not enforce them.

Here is the whole example. It is used for every section below.

```python
def greet(name: str) -> str:
    return "Hi " + name

def first(items: list[int]) -> int | None:
    if items:
        return items[0]
    return None

print(greet("Ana"))
print(first([4, 5]))
print(first([]))
```

```output
Hi Ana
4
None
```

Line 1 says `greet` takes a `str` and gives a `str` back. Python stores the hints in `greet.__annotations__` and does nothing else with them.

## Hints for lists and dictionaries

Containers say what is inside them. A list of numbers is `list[int]`. A dictionary from text to numbers is `dict[str, int]`. The type in the square brackets is the type of the items: for a dictionary, the key type first, then the value type.

## int | None: a value that might be missing

Sometimes a function returns a value, or nothing. Write `int | None` and read the bar as "or": you get a number, or you get `None`. Any code that calls the function has to handle both cases. In the example, `first([4, 5])` gives `4` and `first([])` gives `None`, exactly as the hint promises.

Older code writes the same thing as `Optional[int]`. It means `int | None`, and the bar form needs no import.

## What a type checker does

A type checker reads your hints without running the code. Call `greet(5)` and the checker flags that an `int` was passed where a `str` is expected, before you ever start the program. Tools such as mypy and ty do this job. Python still runs the file either way, so the checker is your safety net, not part of the language.

## The greet and first example, line by line

Line 1 defines `greet`, with `name` as a `str` and a `str` coming back. Line 2 joins `"Hi "` and the name. Line 4 defines `first`, taking a `list[int]` and returning `int | None`. Lines 5 and 6 return the first item if the list has any. Line 7 returns `None` when it is empty. Lines 9 to 11 call both functions and print the results.

## What you learned

- A colon adds a type to a parameter, and an arrow adds a return type.
- Square brackets describe what a container holds: `list[int]`, `dict[str, int]`.
- `int | None` marks a value that might be missing.
- A type checker reads the hints without running your code. Python does not enforce them.

## Common questions

**Does Python check type hints when the code runs?** No. `x: list[int] = ["a"]` runs without an error, and `greet.__annotations__` just stores the hints. A type checker such as mypy is what reports the mismatch.

**Do I need to import anything for `list[int]` and `int | None`?** Not in Python 3.12 and later. Both work with no import. Older tutorials import `List` and `Optional` from `typing`, which you only need for old Python versions.

**What is the difference between `int | None` and `Optional[int]`?** None. In Python 3.14, `Optional[int]` prints as `int | None`. The bar form is shorter and needs no import.

**Do I have to add hints to every function?** No. Hints are optional and you can add them one function at a time. They help most on function signatures that other people call, and where a value might be `None`.

**Which type checker should I use?** mypy is the long-standing choice, and ty is a newer, faster one. Both read the same hints, so the hints you write work with either.

Next in the series: stacks and queues, and how to build both from a list and a deque.
