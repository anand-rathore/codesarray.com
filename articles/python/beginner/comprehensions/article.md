title: Python list comprehensions: lists, dicts, sets, if, any and all
summary: Build a Python list, dictionary or set from another one in a single line, filter it with if, test it with any and all, and know when a plain loop is clearer.
description: Python list comprehensions for beginners: build lists, dicts and sets in one line, filter with if, use any and all, and know when to use a loop.
date: 2026-10-10
read: 4 min read
lesson: 9
video: Comprehensions | https://youtu.be/HwBQ8SM2iGg
image: cover.png
---
A Python list comprehension builds a new list from an old one in a single line. By the end of this page you will write list, dictionary and set comprehensions, filter them with `if`, test a whole collection with `any` and `all`, and know when a plain loop is the clearer choice.

## List comprehensions

Inside square brackets you write the expression first, then `for`, a name, `in`, and the source. `[n * n for n in nums]` gives the square of every number in `nums`. It does the same job as a loop that starts with an empty list and calls `append` on every pass, but it fits on one line and reads left to right.

## Filtering with if

Add an `if` at the end to keep only some items. `[n for n in nums if n % 2 == 0]` keeps the even numbers. Each item is tested first, and only the ones that pass are collected.

## Dictionary and set comprehensions

Curly brackets build other types. With a colon, key then value, you get a dictionary comprehension: `{w: len(w) for w in words}` maps every word to its length. Without a colon you get a set comprehension, and duplicates vanish. The letters of `"hello"` give four unique letters, not five.

## any and all

`any` is `True` if at least one item passes the test. `all` is `True` only if every item passes. Write the test inside the brackets of the call, with no square brackets of its own: `any(n > 4 for n in nums)`. Python checks the items one at a time and stops as soon as the answer is known.

## Comprehension or loop?

A comprehension is for building one collection from another. If you need several steps, a side effect such as `print`, or a nested condition that takes a moment to read, use a plain loop. Short and clear beats clever.

```python
nums = [1, 2, 3, 4, 5]

squares = [n * n for n in nums]
print(squares)

evens = [n for n in nums if n % 2 == 0]
print(evens)

lengths = {w: len(w) for w in ["red", "green"]}
print(lengths)

letters = {c for c in "hello"}
print(len(letters))

print(any(n > 4 for n in nums))
print(all(n > 4 for n in nums))
```

```output
[1, 4, 9, 16, 25]
[2, 4]
{'red': 3, 'green': 5}
4
True
False
```

Line 1 is the list of numbers. Line 3 squares each one with a list comprehension and line 4 prints the result. Line 6 keeps only the evens, and line 7 prints them. Line 9 builds a dictionary from words to their lengths, and line 10 prints it. Line 12 builds a set of letters, and line 13 prints how many there are: four, because the two `l` characters collapse into one. Line 15 asks whether any number is bigger than `4`, which is `True` because of `5`. Line 16 asks whether all of them are, which is `False` because `1` is not.

## What you learned

- A list comprehension builds a list in one line: `[expression for name in source]`.
- An `if` at the end filters which items are kept.
- Curly brackets with a colon make a dictionary, and without a colon make a set.
- `any` and `all` test a whole collection and stop as soon as the answer is known.
- When it gets complicated, a plain loop is the better choice.

## Common questions

**Is a list comprehension faster than a for loop?** Usually a little, because Python does not look up and call `append` on every pass. Choose it for readability first; the speed difference rarely matters.

**Can I use if and else in a comprehension?** Yes, but the order changes. A filter goes at the end: `[n for n in nums if n > 2]`. A choice between two values goes at the front: `[n if n > 2 else 0 for n in nums]`.

**Can I write one comprehension inside another?** Yes. `[x for row in grid for x in row]` flattens a list of lists. If it takes more than a moment to read, write the loops out instead.

**How do I make an empty set?** `{}` is an empty dictionary. Use `set()` for an empty set.

**Does the loop variable leak out of the comprehension?** No. After `[k for k in nums]`, using `k` raises a `NameError`, because the name lives only inside the comprehension.

This lesson follows on from [Python functions](/articles/python/beginner/functions/). Next in the series: errors and exceptions.
