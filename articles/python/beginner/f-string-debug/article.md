title: Python f-string debugging: print the name and value with =
summary: Put an equals sign after a name inside an f-string and Python prints the name, the equals sign and the value, so debug prints never need the name typed twice.
description: Python f-string debugging with =: f"{price=}" prints price=4.5, the name and the value together, and it works on expressions like price * count in Python 3.8 and later.
date: 2026-10-08
read: 2 min read
follows: 4
video: Debug with an f-string equals sign | https://youtube.com/shorts/ooq6sgWcCOM
image: cover.png
---
Python f-string debugging takes one character: put an `=` after a name inside the braces and the f-string prints the name and its value together. You stop typing the variable name twice in every debug print.

## The name and the value

```python
price = 4.5
count = 3
total = price * count
print(f"{price=}")
print(f"{count=}")
print(f"{total=}")
```

```output
price=4.5
count=3
total=13.5
```

`f"{price=}"` prints the text you wrote (`price`), then the equals sign, then the value. The label always matches the code, so a debug print cannot say `prise` while showing `price`.

## It works on expressions

```python
print(f"{price * count=}")
```

```output
price * count=13.5
```

Whatever you write before the `=` is printed as written and then evaluated, so you see both the expression and its result.

## When to use it

- Quick debug prints while you work out why a value is wrong.
- Checking an intermediate calculation without naming it.
- It needs Python 3.8 or later.

Because the print is one short line, it is also easy to delete when you are done.

This is a short note on [Strings](/articles/python/beginner/strings/), lesson 4 of the Python beginner track.
