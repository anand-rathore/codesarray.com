title: Python variables and data types: int, float, str, bool, None
summary: The five basic types, how to ask Python what type a value is, and how to turn one type into another.
description: Python variables and data types for beginners: int, float, str, bool and None, the type() function, dynamic typing, and how to convert between types.
date: 2026-10-05
read: 5 min read
lesson: 2
video: Variables and types | https://youtu.be/goptyPZ-XuM
image: cover.png
---
Every value in Python has a data type. By the end of this page you will know the five basic Python data types, how to ask Python what type a value is with the `type()` function, and how to turn one type into another.

## What a variable is

A variable is a name for a value. Write the name, an equals sign, and the value:

```python
score = 10
```

Python stores `10` and calls it `score`. There is no keyword and no type to declare. Use the name and you get the value back. Assign again and the name points to the new value:

```python
print(score)
score = score + 5
print(score)
```

```output
10
15
```

## The five basic types

Every value has a type.

- `42` is an **int**: a whole number.
- `3.14` is a **float**: a number with a decimal point.
- `"hello"` is a **str**, short for string: text in quotes.
- `True` and `False` are **bool**.
- `None` means no value at all.

Ask Python with the `type` function and it tells you:

```
>>> type(42)
<class 'int'>
```

## Dynamic typing

The type belongs to the value, not to the name. So the same name can hold a number now and text later:

```python
x = 5
x = "five"
```

Python checks types while the program runs. That is called dynamic typing.

## Arithmetic

Plus, minus and times work as you expect. Division has two forms, and the difference matters:

```
>>> 7 / 2
3.5
>>> 7 // 2
3
>>> 7 % 2
1
>>> 2 ** 10
1024
```

A single slash always gives a float. A double slash drops the fraction. Percent gives the remainder, and two stars is a power.

## Comparisons and logic

A comparison asks a question and answers with a bool. A double equals tests whether two values are equal; a single equals assigns. Combine answers with `and`, `or` and `not`:

```
>>> age = 36
>>> is_admin = True
>>> age >= 18
True
>>> age == 36
True
>>> age >= 18 and not is_admin
False
```

## Converting between types

Types do not mix by themselves. Adding text to a number is an error:

```
>>> "3" + 4
```

```output
TypeError: can only concatenate str (not "int") to str
```

Convert first. `int` turns text into a whole number, `str` turns a number into text, and `float` handles decimals:

```
>>> int("3") + 4
7
>>> "3" + str(4)
'34'
>>> float("3.5")
3.5
```

## The whole program

```python
name = "Ada"
age = 36
height = 1.68
is_admin = True
nickname = None

print(type(name), type(age))
next_year = age + 1
half = age / 2
print(next_year, half)

print(age >= 18 and not is_admin)
print("Age: " + str(age))
print(int("42") + 8)
```

Lines 1 to 5 store five values, one of each type. Line 7 prints two of the types. Line 8 adds one to `age` and line 9 halves it; the slash makes a float. Line 12 asks a question and prints the answer. Line 13 converts `age` to text so it can join the label, and line 14 converts text to a number before adding.

```output
<class 'str'> <class 'int'>
37 18.0
False
Age: 36
50
```

## What you learned

- `int`, `float`, `str`, `bool` and `None` are the basic types.
- `type(x)` tells you which one you have.
- `7 / 2` gives a float; `7 // 2` gives a whole number.
- Comparisons give a bool.
- `int()`, `float()` and `str()` convert between types.

## Common questions

**Why does `7 / 2` give `3.5` and not `3`?** In Python a single slash is true division and always gives a float, even when the numbers divide exactly: `8 / 2` is `4.0`. When you want the whole-number part, use `//`, which gives `3` for `7 // 2`.

**Why does my number print as `18.0` instead of `18`?** Because it came from a division. `age / 2` is a float, so it prints with a decimal point. Use `age // 2` if you want an int, or `int(age / 2)` to convert the result.

**What is the difference between `=` and `==`?** A single equals assigns: `age = 36` stores 36 under the name `age`. A double equals compares: `age == 36` asks whether `age` is 36 and answers `True` or `False`. Writing `=` where you meant `==` inside an `if` is a syntax error, so Python will tell you.

**Is `None` the same as `0` or an empty string?** No. `None` is its own value, meaning "nothing here". `None == 0` is `False`, and so is `None == ""`. Use `None` when a variable has no value yet, and a real `0` or `""` when the value is genuinely zero or empty.

**Do I have to declare a type like in other languages?** No. The type belongs to the value, and Python reads it from the value you assign. The same name can hold an int now and a str later. That freedom is why conversions matter: Python will not guess what you meant by `"3" + 4`.

This lesson follows on from [Your first Python program](/articles/python/beginner/your-first-python-program/). Next in the series: control flow.
