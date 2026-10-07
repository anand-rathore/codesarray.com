title: Python chained comparison: 0 < x < 10 just works
summary: In most languages that line is a bug. In Python it is one test that means exactly what it says, and this note shows how Python reads it.
description: Python chained comparison explained: why 0 < x < 10 works, how it equals 0 < x and x < 10 with x checked once, and what x == y == z means.
date: 2026-10-07
read: 2 min read
follows: 3
video: Chained comparisons | https://youtube.com/shorts/DsRjN1hBeP0
image: cover.png
---
In most languages, `0 < x < 10` is a bug: the first comparison gives a boolean, and that boolean is then compared with 10. In Python it is a chained comparison, and it is just how you write it.

## One chain, two tests

```python
x = 5
print(0 < x < 10)
print(0 < x and x < 10)
x = 15
print(0 < x < 10)
print(1 < 3 > 2)
```

```output
True
True
False
True
```

`0 < x < 10` is exactly the same test as `0 < x and x < 10`. With `x` at 5 both are `True`. Set `x` to 15 and the chain is `False`, because the second half fails. The last line shows that the operators do not even have to point the same way: `1 < 3 > 2` asks whether 3 is bigger than both its neighbours, and it is.

## How Python reads a chain

Python reads `a < b < c` as `a < b and b < c`, with one difference from writing it out yourself: the middle value is evaluated once. If `b` is a function call, it is called one time, not two.

The same rule applies to every comparison operator, so `x == y == z` asks whether all three values are equal, and `a <= b < c` is a half-open range check. Every link in the chain has to be `True` for the whole chain to be `True`.

## What to take from this

- Write a range check the way you would on paper: `0 < x < 10`.
- It means `0 < x and x < 10`, with `x` checked once.
- Any comparisons chain, including `==`, and the directions can mix.

This is a short note on [Control flow](/articles/python/beginner/control-flow/), lesson 3 of the Python beginner track.
