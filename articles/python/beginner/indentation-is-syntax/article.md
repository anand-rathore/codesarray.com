title: Python has no braces: the whitespace is the code
summary: Why four spaces decide what your program does, shown with one line that moves.
date: 2026-10-05
read: 3 min read
follows: 1
video: Hello, Python | https://youtu.be/NExcPTw_LvQ
aliases: /articles/python-indentation-is-syntax/
---
Most languages mark a block of code with curly braces. Python does not have them. It decides which lines belong to an `if` by how far they are indented, so moving a line sideways changes what the program does.

## Five lines

```python
age = 12
if age >= 18:
    print("adult")
    print("can vote")
print("done")
```

Line 2 asks: is `age` at least 18? Lines 3 and 4 are indented under the `if`, so they belong to it. Twelve is not at least eighteen, so both are skipped, and the program prints one line:

```output
done
```

## Move one line

Now delete four spaces from line 4. Nothing else changes.

```python
age = 12
if age >= 18:
    print("adult")
print("can vote")
print("done")
```

That line has left the block. It no longer depends on the `if`, so it always runs:

```output
can vote
done
```

A twelve-year-old can vote. The words in the file are identical; only the whitespace moved.

## What to take from this

- The indentation is not decoration. It is how Python knows where a block starts and ends.
- A block ends at the first line that goes back to the left.
- Use four spaces per level, and never mix tabs and spaces in one file.
- If a line should depend on an `if`, a loop or a function, check that it is indented under it. This is the first thing to look at when a program runs the wrong lines.

What you see is what runs. That is the trade Python makes: no braces to match, and in return the layout has to be right.

New to Python? Start with [Your first Python program](/articles/python/beginner/your-first-python-program/).
