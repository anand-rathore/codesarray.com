title: Python tuples and sets: unpacking, swapping and removing duplicates
summary: Make a Python tuple, unpack it, swap two variables in one line, and use a set to remove duplicates and check membership in O(1).
description: Python tuples and sets for beginners: unpack with x, y = point, swap with a, b = b, a, drop duplicates with set(), and why in is O(1) on a set.
date: 2026-10-09
read: 5 min read
lesson: 6
video: Tuples and sets | https://youtu.be/6pZflf0qQ_A
image: cover.png
---
A tuple is a list that never changes, and a set is a collection that holds each value once. By the end of this page you will make a tuple, unpack it into names, swap two variables in one line, remove duplicates with a set, and know why the `in` test is so much faster on a set than on a list.

## Tuples: round brackets, never change

A tuple is written with round brackets, and you index it just like a list: `point = (3, 4)` gives `point[0]` as `3`. The difference is that it can never change. `point[0] = 9` raises `TypeError: 'tuple' object does not support item assignment`. Use a tuple for a small, fixed record, such as a coordinate, where the pieces belong together.

## Unpacking and swapping

Unpacking pulls a tuple apart into names: `x, y = point` gives `x` the `3` and `y` the `4`. The number of names has to match the number of items. The same idea swaps two variables in one line: `a, b = b, a`. No temporary variable is needed.

## Sets: each value once, no order

A set holds each value once. Pass a list to `set()` and the repeats are gone. A set has no order, so you cannot index it: `{1, 2}[0]` raises `TypeError: 'set' object is not subscriptable`. `add()` puts a new item in, and adding one that is already there changes nothing.

```python
point = (3, 4)
x, y = point
print(x, y)
x, y = y, x
print(x, y)

tags = ["py", "go", "py", "js", "go"]
unique = set(tags)
print(len(unique))
print(sorted(unique))
print("js" in unique)
```

```output
3 4
4 3
3
['go', 'js', 'py']
True
```

Line 2 unpacks the tuple and line 3 prints `3 4`. Line 4 swaps the two and line 5 prints `4 3`. Line 8 turns the list with five items into a set, and line 9 shows only three are left. Line 10 prints them sorted, because a set has no order of its own to print. Line 11 asks whether `"js"` is in the set.

## Why in is fast on a set

Asking whether `"js"` is in a list checks the items one by one, so it is O(n). A set jumps straight to the answer, O(1), even with a million items, because it uses a hash table: the value itself points to its slot. That is why a set is the fast way to check membership, and why turning a list into a set is the quick way to remove duplicates.

## What you learned

- A tuple is an ordered collection in round brackets that never changes.
- `x, y = point` unpacks a tuple, and `a, b = b, a` swaps two values.
- A set holds each value once, with no order, so you cannot index it.
- `set(tags)` removes duplicates, and `add()` puts a new item in.
- `in` is O(1) on a set and O(n) on a list.

## Common questions

**How do I make an empty set?** Use `set()`. Empty curly braces, `{}`, make an empty dictionary, not a set.

**How do I make a tuple with one item?** Add a trailing comma: `(5,)` is a tuple, while `(5)` is just the number `5`.

**Does `set()` keep the order of my list?** No. If you need the duplicates gone and the first-seen order kept, use `list(dict.fromkeys(tags))`, which gives `['py', 'go', 'js']`.

**Can a tuple contain a list?** Yes, and the list inside can still change. The tuple only guarantees that it keeps pointing at the same items.

**Can I use a tuple as a set item?** Yes. Tuples never change, so they can go in a set. Lists cannot.

This lesson follows on from [Python lists](/articles/python/beginner/lists/). Next in the series: dictionaries.
