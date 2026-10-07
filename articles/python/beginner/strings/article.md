title: Python strings: indexing, slicing, methods and f-strings
summary: Pick characters out of a Python string, slice pieces off it, clean it up with methods like strip and split, and build new text with f-strings.
description: Python strings for beginners: index with word[0], slice with word[::-1], clean text with strip and split, and build text with f-strings.
date: 2026-10-07
read: 5 min read
lesson: 4
video: Strings | https://youtu.be/x7J8t9UehDA
image: cover.png
---
Python strings are text you can index, slice, clean up and format. By the end of this page you will pick characters out of a string, slice pieces off it, tidy it with methods like `strip()` and `split()`, and build new text with f-strings.

## Index and slice a string

A string is a sequence of characters, and each one has a position counted from zero. Negative positions count from the end, and `len()` tells you how many characters there are. A slice takes a piece: `word[0:3]` runs from 0 up to, but not including, 3. Leave out the start and it begins at the beginning, leave out the end and it runs to the end. A third number is the step, and a step of `-1` walks backwards:

```python
word = "Python"
print(word[0], word[-1])
print(word[0:3], word[2:])
print(word[::-1])
```

```output
P n
Pyt thon
nohtyP
```

`word[0]` is the first letter and `word[-1]` the last. `word[0:3]` is `Pyt`, `word[2:]` is `thon`, and `word[::-1]` is the whole word reversed.

## Strings are immutable

You cannot change a character in place:

```python
word[0] = "J"
```

```output
TypeError: 'str' object does not support item assignment
```

A string never changes after it is made. Every method that looks like it changes one actually returns a new string. `word.upper()` gives `'PYTHON'`, but `word` is still `'Python'`. If you want the new value, assign it back, as the next section does with `name = name.strip()`.

## Python string methods: strip, split, replace

Strings come with dozens of methods. `strip()` removes spaces at both ends, `upper()` and `lower()` change the case, `split()` cuts a string into a list at a separator, `join()` glues a list back together with the string you call it on, and `replace()` swaps one piece of text for another. The `in` test tells you whether a piece is there at all:

```python
name = "  Ada Lovelace  "
name = name.strip()
print(name.upper())
print(name.split(" "))
print(name.replace("Ada", "A."))
```

```output
ADA LOVELACE
['Ada', 'Lovelace']
A. Lovelace
```

Because strings are immutable, line 2 assigns the stripped text back to `name`. The three prints then work on the cleaned string and leave it unchanged.

## Build text with f-strings

To build text from values, put an `f` before the quotes. Anything in curly braces is evaluated and dropped into the text, and any expression works, such as `{age + 1}`. After a colon you say how to format it: `:.2f` rounds to two decimal places and `:,` adds thousands separators. Put an equals sign inside the braces and Python prints the name and the value together, which is handy for debugging:

```python
age = 36
print(f"{name} is {age}")
print(f"{age=}")
print(f"{age / 7:.2f}")
```

```output
Ada Lovelace is 36
age=36
5.14
```

`name` still holds `Ada Lovelace` from the last section. `f"{age=}"` printed `age=36`, and `age / 7` is 5.142857..., rounded to `5.14`.

## A glance at t-strings

Python 3.14 added t-strings: the same syntax with a `t` instead of an `f`. A t-string does not give you text. It gives a `Template` object that keeps the pieces of text and the values separate, so a library can escape them safely before building HTML or SQL:

```python
name = "Ada"
t = t"Hello {name}"
print(t.strings, t.values)
```

```output
('Hello ', '') ('Ada',)
```

You do not need them yet. For everyday text, f-strings are what you want.

## What you learned

- `word[0]` picks a character and negative numbers count from the end.
- `word[1:4]` slices a piece, and a step of `-1` reverses the string.
- Strings are immutable: methods return new strings, so assign the result back.
- `strip()`, `split()`, `join()` and `replace()` do most of the everyday cleaning.
- f-strings put values into text, with a format after a colon and `{x=}` for debugging.

## Common questions

**What happens if I index past the end?** `"Python"[10]` raises `IndexError: string index out of range`. A slice is more forgiving: `"Python"[2:100]` gives `'thon'` and `"Python"[10:]` gives an empty string.

**What is the difference between split() and split(" ")?** With no argument, `split()` treats any run of spaces as one gap, so `"a  b   c".split()` gives `['a', 'b', 'c']`. `split(" ")` cuts at every single space and keeps the empty pieces: `['a', '', 'b', '', '', 'c']`.

**Why does "age: " + 36 fail?** Python will not guess how to join text and a number. It raises `TypeError: can only concatenate str (not "int") to str`. Use an f-string instead: `f"age: {36}"`.

**Does len() count letters or bytes?** It counts characters, so `len("héllo")` is 5 and `len("🐍")` is 1.

**How do I remove spaces from only one end?** Use `lstrip()` for the left end and `rstrip()` for the right. Give any of the three a string such as `"xxhixx".strip("x")` and it removes those characters instead of spaces.

This lesson follows on from [Python if else and loops](/articles/python/beginner/control-flow/). Next in the series: lists.
