title: Python iterators and generators: yield, next and itertools
summary: What a for loop really does with iter and next, how yield turns a function into a generator, why a generator expression uses almost no memory, and the lazy tools in itertools.
description: Python iterators and generators explained: iter and next, yield, generator expressions that save memory, why a generator runs once, and itertools count, islice and chain.
date: 2026-10-15
read: 4 min read
lesson: 2
video: Iterators and Generators in Python | https://youtu.be/bTNl4SKsV30
image: cover.png
---
By the end of this page you will know what a Python `for` loop does behind the scenes, be able to write your own generator with `yield`, and understand why a generator can process a million items without holding them all in memory.

## Python iterators: what a for loop really does

Every `for` loop runs on one idea. Python calls `iter()` on the thing you loop over and gets an iterator back. Then it calls `next()` again and again. Each call hands you one item and remembers where it was. When there is nothing left, `next()` raises `StopIteration`, and the loop quietly ends.

A list is iterable, but it is not an iterator itself. `iter(nums)` gives you one, and that is the object that remembers the position.

## Generators: yield pauses a function

You can write your own iterator with a function. Put `yield` inside it and it becomes a generator function. Calling it does not run the body. It hands you a generator. Each `next()` runs the body until the next `yield`, gives you that value, and pauses with all its variables intact. The next call resumes on the very next line. When the body ends, the loop is over.

## Generator expressions: lazy and small

A list comprehension with square brackets builds every value up front. The same expression in parentheses is a generator expression. It holds only its place, and makes each value when something asks for it.

For a million squares, measured with `sys.getsizeof`, the list is 8,448,728 bytes and the generator is 208. The catch is that a generator can be used once. Loop over it a second time and it is empty.

## itertools: lazy building blocks

The `itertools` module is a toolbox of lazy pieces:

- `count(1)` gives numbers forever.
- `islice(count(1), 5)` takes just the first five, so `list(islice(count(1), 5))` is `[1, 2, 3, 4, 5]`.
- `chain([1, 2], "ab")` joins several iterables into one stream.

None of them build a list, so you can pipe them together and nothing is computed until you ask. That is how you can describe an endless sequence, take only the part you need, and never pay for the rest.

## The countdown generator, line by line

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

steps = countdown(3)
print(next(steps))
print(next(steps))
print(list(steps))
print(list(steps))
```

`countdown` loops while `n` is above zero. The `yield` hands `n` to the caller and pauses. The `n -= 1` line only runs when the next value is asked for. `countdown(3)` runs nothing yet. The two `next()` calls give 3 and 2. `list(steps)` collects what is left, which is just 1. The last line tries again, and the generator is used up, so the list is empty.

```output
3
2
[1]
[]
```

## What you learned

- A `for` loop calls `iter()` once, then `next()` until `StopIteration`.
- A function with `yield` is a generator, and it pauses between values.
- Parentheses instead of square brackets give a lazy generator expression.
- `itertools` lets you build pipelines that never hold the whole data.
- A generator is single use.

## Common questions

**What is the difference between an iterable and an iterator?** An iterable is anything you can loop over, like a list. An iterator is the object that does the looping and remembers the position. `iter()` turns an iterable into an iterator.

**Does a generator run when I call the function?** No. Calling a generator function returns a generator and runs none of the body. The body starts on the first `next()`.

**Why is my generator empty the second time?** It was used up. A generator produces each value once. If you need the values again, call the function again, or build a list.

**When should I use a list instead?** When you need the values more than once, need `len()`, or need to index into them. Use a generator when you only need to pass over the values one time.

**Is a generator faster than a list?** Not by itself. It saves memory, and it can stop early. Building the whole list can be faster for small data.

Next in the series: closures and scope, and how a function can remember the variables around it.
