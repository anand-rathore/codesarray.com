title: Reverse a string in Python with slicing: [::-1]
summary: Slice a Python string with a step of minus one and you get it backwards, with no loop and no function. The same trick checks for a palindrome.
description: Reverse a string in Python with slicing: word[::-1] needs no loop and no function, and name == name[::-1] checks a palindrome. Works on any string.
date: 2026-10-08
read: 2 min read
follows: 4
video: Reverse a string in Python | https://youtube.com/shorts/VpUdOuLBHx0
image: cover.png
---
To reverse a string in Python, slice it with a step of minus one: `word[::-1]`. There is no loop and no function to call, just three characters after the name.

## Reverse with [::-1]

```python
word = "stressed"
print(word[::-1])
```

```output
desserts
```

A slice has three parts, `start:stop:step`. Leaving start and stop empty means the whole string, and a step of `-1` walks it backwards, one character at a time.

## Check a palindrome

```python
name = "level"
print(name[::-1])
print(name == name[::-1])
```

```output
level
True
```

A palindrome reads the same both ways, so comparing a string to its reverse tells you whether it is one.

## Things to know

- Strings never change, so `[::-1]` returns a new string and the original stays as it was.
- It works on any string, and on lists and tuples too.
- Case and spaces count, so `"Level"` is not equal to its reverse.

This is a short note on [Strings](/articles/python/beginner/strings/), lesson 4 of the Python beginner track.
