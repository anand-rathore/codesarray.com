title: Python int overflow: why 2 ** 1000 just works
summary: Most languages keep a whole number in 64 bits and overflow past it. A Python int has no limit, and the reason also explains why floats still do.
description: Python int overflow does not happen: 2 ** 63, 2 ** 64 and 2 ** 1000 print in full as ordinary ints. Why ints grow without limit while 2.0 ** 1024 raises OverflowError.
date: 2026-10-06
read: 2 min read
follows: 2
video: Ints never overflow | https://youtube.com/shorts/k4eOUnpWxTY
image: cover.png
---
Most languages keep a whole number in 64 bits. Go past about 9 quintillion, 9223372036854775807 to be exact, and the number overflows: in Java it wraps around to a negative value, in C the result is undefined. Python int overflow is not a thing. A Python int just keeps counting, and this note shows how far and why.

## Past 64 bits, still an int

```python
print(2 ** 63)
print(2 ** 64)
big = 2 ** 1000
print(len(str(big)))
print(type(big))
```

```output
9223372036854775808
18446744073709551616
302
<class 'int'>
```

`2 ** 63` is the first number a signed 64-bit integer cannot hold. Python prints it. `2 ** 64` goes one bit further, and Python prints that too. `2 ** 1000` has 302 digits, and `type(big)` shows it is still an ordinary `int`, the same type as `3`. There is no separate "big integer" type to ask for.

## Why: an int is not a fixed box

In most languages an integer is a fixed box of 64 bits, so there is a largest value it can hold. A Python int is stored in as many chunks as it needs, and Python adds more chunks as the number grows. Memory is the only limit, which in practice means none. The cost is a little speed: arithmetic on a number that spans several chunks takes longer than one machine instruction, which is why Python is slower than C at raw number crunching and why that almost never matters.

## Floats are the fixed box

```python
print(2.0 ** 1000)
print(2.0 ** 1024)
```

```output
1.0715086071862673e+301
OverflowError: (34, 'Result too large')
```

A float is always 64 bits, so it does have a largest value: a little under `1.8e308`. `2.0 ** 1000` fits. `2.0 ** 1024` does not, and because there is nowhere for it to go Python raises `OverflowError` rather than quietly returning something wrong. The second line is the last line of the traceback.

## What to take from this

- `int` has no upper limit. `2 ** 1000` is as ordinary as `2 ** 3`.
- Python stores an int in as many chunks as it needs, and the only cost is a little speed.
- `float` is a fixed 64-bit box, so `2.0 ** 1024` raises `OverflowError`.

This is a short note on [Variables and types](/articles/python/beginner/variables-and-types/), lesson 2 of the Python beginner track.
