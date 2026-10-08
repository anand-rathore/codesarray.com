title: Python lists: index, slice, append, pop and sort
summary: Build a Python list, index and slice it, grow and shrink it with append, insert and pop, sort it, and learn what each move costs.
description: Python lists for beginners: index with nums[0], slice with nums[1:3], use append, insert, pop and sort, and avoid the b = a copy trap.
date: 2026-10-08
read: 5 min read
lesson: 5
video: Lists | https://youtu.be/YTe0ls2tLTM
image: cover.png
---
A Python list is an ordered collection you can index, slice, grow, shrink and sort. By the end of this page you will build a list, pick items out of it, change it with `append()`, `insert()`, `pop()` and `sort()`, know which of those are fast, and avoid the trap where `b = a` is not a copy.

## Create, index and slice a list

A list is written in square brackets, and like a string, each item has a position counted from zero. Negative positions count from the end, `len()` tells you how many items there are, and a slice such as `nums[1:3]` runs from 1 up to, but not including, 3. Unlike a string, a list is mutable: `nums[0] = 5` changes the item in place. Asking for a position past the end raises `IndexError: list index out of range`.

## Grow and shrink a list

`append()` adds one item to the end. It is fast, O(1), because Python keeps spare room at the end of the list. `insert()` puts an item at any position, but every item after it has to shift along, so it costs O(n). `pop()` with no argument removes and returns the last item, which is O(1). `pop(0)` takes the first item, and then everything shifts down, so that one is O(n).

```python
nums = [30, 10, 20]
nums.append(40)
nums.insert(0, 5)
print(nums)
print(nums[0], nums[-1])
print(nums[1:3])

last = nums.pop()
print(last, nums)
nums.sort()
print(nums)
print(20 in nums)
```

```output
[5, 30, 10, 20, 40]
5 40
[30, 10]
40 [5, 30, 10, 20]
[5, 10, 20, 30]
True
```

Lines 2 and 3 grow the list, line 4 shows `[5, 30, 10, 20, 40]`, and lines 5 and 6 print the two ends and the slice. Line 8 pops `40` into `last`, line 10 sorts the list in place, and line 12 asks whether `20` is in it.

## sort, sorted and the in test

`sort()` orders the list in place and returns `None`, so `nums = nums.sort()` leaves you with `None` instead of a list. If you want a new sorted list and want to keep the original, use the function `sorted()`. Pass `reverse=True` to go from largest to smallest, or `key=len` to sort by length.

The `in` test checks the items one by one from the left, so it is O(n). If you test membership a lot, a set is faster, and sets are coming in the next lesson.

## Why b = a is not a copy

`b = a` does not copy a list. It gives the same list a second name:

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
c = a.copy()
c.append(5)
print(a, c)
```

```output
[1, 2, 3, 4]
[1, 2, 3, 4] [1, 2, 3, 4, 5]
```

Appending to `b` changed `a` too, because there is only one list. `a.copy()`, or the slice `a[:]`, makes a real copy, so appending to `c` leaves `a` alone.

## What you learned

- A list is an ordered, mutable collection in square brackets.
- `nums[0]` indexes, `nums[-1]` counts from the end, and `nums[1:3]` slices.
- `append()` and `pop()` at the end are O(1); `insert()` and `pop(0)` shift everything, so they are O(n).
- `sort()` changes the list and returns `None`; `sorted()` returns a new list.
- `b = a` is not a copy: use `a.copy()`.

## Common questions

**What happens if I pop from an empty list?** `[].pop()` raises `IndexError: pop from empty list`. Check the list first with `if nums:` when it might be empty.

**Is slicing past the end an error?** No. With `nums = [30, 10, 20]`, `nums[1:100]` gives `[10, 20]` and `nums[10:]` gives an empty list. Only a single index such as `nums[10]` raises `IndexError`.

**How do I remove an item by value?** Use `remove()`: `nums.remove(10)` deletes the first `10` it finds and returns `None`. If the value is not there it raises `ValueError: list.remove(x): x not in list`.

**Can a list hold different types?** Yes. `[1, "two", 3.0, [4]]` is a valid list, and it can even contain another list.

**Does `copy()` copy the lists inside a list?** No, it makes a shallow copy. With `a = [[1], [2]]` and `b = a.copy()`, appending to `b[0]` also changes `a[0]`, because both outer lists hold the same inner list.

This lesson follows on from [Python strings](/articles/python/beginner/strings/). Next in the series: tuples and sets.
