title: Python if else and loops: if, elif, for, while, break, continue
summary: How a program decides with if, elif and else, repeats with for and while, and stops or skips a round with break and continue.
description: Python if else and loops for beginners: if, elif and else, chained comparisons, for over range(), while, break, continue, and the else a loop can have.
date: 2026-10-06
read: 5 min read
lesson: 3
video: Control flow | https://youtu.be/NqTma5wsLjs
image: cover.png
---
Python if else and loops are how a program decides what to do and does it again. By the end of this page your programs will make decisions with `if`, `elif` and `else`, repeat work with `for` and `while`, and stop a loop early with `break` or skip one round with `continue`.

## Decide with if, elif and else

Write `if`, a condition, and a colon. The indented lines run only when the condition is `True`. `elif` checks another condition if the first one was `False`, and `else` catches everything that is left:

```python
temperature = 23
if temperature > 30:
    print("hot")
elif 20 <= temperature <= 30:
    print("warm")
else:
    print("cold")
```

```output
warm
```

Python tries the conditions in order, runs the first block that matches, and skips the rest. `temperature` is 23, so the first test fails, the second passes, and only `warm` is printed.

## Chained comparisons

That middle condition, `20 <= temperature <= 30`, is a chained comparison. In most languages you would write two comparisons joined by `and`:

```python
20 <= temperature and temperature <= 30
```

Python lets you write it the way you would on paper, and it means exactly the same thing. Any comparisons chain this way:

```
>>> 0 < 5 < 10
True
>>> 0 < 15 < 10
False
```

## Repeat with for

A `for` loop repeats a block once for each item in a sequence. `range(1, 6)` gives the numbers from 1 up to, but not including, 6:

```python
for n in range(1, 6):
    print(n)
```

```output
1
2
3
4
5
```

So `n` takes 1, 2, 3, 4, 5 and the block runs five times. A `for` loop works on any collection: `for word in ["red", "green", "blue"]:` visits each word, and `for letter in "abc":` visits each letter.

## Repeat with while

A `while` loop repeats as long as a condition stays `True`:

```python
count = 3
while count > 0:
    print(count)
    count -= 1
```

```output
3
2
1
```

`count` starts at 3. Each time round, the loop prints `count` and subtracts one. When `count` reaches 0, the condition `count > 0` is `False` and the loop ends. Make sure something inside the loop changes the condition, or it runs forever.

## break and continue

Two keywords change a loop from inside. `continue` skips the rest of this round and goes straight to the next item:

```python
for n in range(1, 6):
    if n == 3:
        continue
    print(n)
```

```output
1
2
4
5
```

`break` stops the whole loop at once:

```python
for word in ["red", "green", "blue"]:
    if word == "green":
        print("found", word)
        break
```

```output
found green
```

The loop ends as soon as it finds `green`, so `blue` is never visited.

## The else on a loop

A loop can have an `else` too. Its block runs only when the loop finished without a `break`:

```python
for word in ["red", "green", "blue"]:
    if word == "green":
        print("found", word)
        break
else:
    print("not found")
```

```output
found green
```

Searching for `green`, `break` fires, so the `else` is skipped. If `green` were not in the list, say `["red", "blue"]`, the loop would run out of words and the `else` would print `not found`. It is Python's way of saying the search failed.

## The whole program

```python
temperature = 23
if temperature > 30:
    print("hot")
elif 20 <= temperature <= 30:
    print("warm")
else:
    print("cold")

for n in range(1, 6):
    if n == 3:
        continue
    print(n)

count = 3
while count > 0:
    print(count)
    count -= 1
```

Lines 2 to 7 decide between hot, warm and cold, and line 4 is the chained comparison. Lines 9 to 12 loop over 1 to 5, and line 11 skips the 3. Lines 14 to 17 count down from 3 with `while`, and line 17 is what makes the loop end.

```output
warm
1
2
4
5
3
2
1
```

## What you learned

- `if`, `elif` and `else` choose one block: the first condition that is `True` wins.
- A chained comparison like `0 < x < 10` reads like maths and means the same as two tests joined by `and`.
- `for` repeats once per item; `while` repeats while a condition holds.
- `break` stops a loop, `continue` skips to the next round.
- A loop's `else` runs only when there was no `break`.

## Common questions

**Why does `range(5)` stop at 4?** `range` counts from the start up to, but not including, the end, and the start is 0 when you give only one number, so `range(5)` is 0, 1, 2, 3, 4. A third number is the step: `range(1, 10, 2)` gives 1, 3, 5, 7, 9.

**What happens if I write `if x = 3:`?** Python refuses to run it. A single equals assigns, a double equals compares, and in Python 3.14 the error message even suggests the fix: `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?`

**When should I use while instead of for?** Use `for` when you know what you are looping over: a range, a list, a string. Use `while` when you do not know in advance how many rounds it will take, such as reading input until the user types `quit` or halving a number until it drops below 1.

**Does break leave every loop I am inside?** No, only the innermost one. The outer loop carries on with its next item. To leave both, put the inner loop in a function and `return` from it.

**Can a while loop have an else as well?** Yes, with the same rule: the `else` runs when the condition became `False` on its own, and is skipped when a `break` ended the loop.

This lesson follows on from [Variables and types](/articles/python/beginner/variables-and-types/). Next in the series: strings.
