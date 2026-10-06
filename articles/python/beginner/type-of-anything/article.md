title: Python knows the type: 3, 3.0 and "3" are not the same
summary: Three values that look alike are an int, a float and a str. type() shows the difference, and mixing them shows why it matters.
date: 2026-10-06
read: 2 min read
follows: 2
video: Python knows the type | https://youtube.com/shorts/Tdcc6wRlv_M
image: cover.png
---
Three, three point zero, and three in quotes look alike. Python knows they are three different things, and you never had to say so.

## Ask it with type()

```python
print(type(3))
print(type(3.0))
print(type("3"))
print(type(True))
print(type(None))
```

```output
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

`3` is an int, a whole number. `3.0` is a float. `"3"` is a str, text. `True` is a bool, and `None` is its own type. You never declared any of this: Python worked it out from the value.

## It matters when you mix them

```
>>> 3 + 3.0
6.0
>>> 3 + "3"
```

```output
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

A number plus a float gives a float. A number plus text is an error, because Python will not guess whether you wanted `6` or `"33"`. Convert first, and say which:

```
>>> int("3") + 3
6
>>> str(3) + "3"
'33'
```

## What to take from this

- The type is in the value. A name has no type of its own.
- `type(x)` tells you what Python sees.
- Values of different types do not combine by themselves. Convert with `int()`, `float()` or `str()` first.

This is a short note on [Variables and types](/articles/python/beginner/variables-and-types/), lesson 2 of the Python beginner track.
