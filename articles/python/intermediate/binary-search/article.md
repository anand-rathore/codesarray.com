title: Python binary search explained: low, high and mid
summary: How binary search works in Python: check the middle of a sorted list, drop half, move low and high past the middle, and why a million items take about 20 steps.
description: Python binary search explained: write a find function with low, high and mid, avoid the off-by-one trap, and see why it takes about log n steps.
date: 2026-10-17
read: 4 min read
lesson: 10
video: Python Binary Search Explained | https://youtu.be/y--kDdf5zdU
image: cover.png
---
By the end of this page you will be able to write binary search in Python, explain why it only works on a sorted list, and say why it is so much faster than checking every item. It builds on [Python recursion](/articles/python/intermediate/recursion/), since both solve a big problem by shrinking it.

## What is binary search in Python

Binary search finds an item in a sorted list by halving the problem. Checking every item one by one is O(n). But if the list is sorted, you can look at the middle item first. If it is too small, the target must be on the right, so the whole left half is gone. If it is too big, drop the right half. Each check throws away half of what is left.

Here is the whole example. It is used for every section below.

```python
def find(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


nums = [2, 5, 8, 12, 16, 23, 38]
print(find(nums, 23))
print(find(nums, 7))
```

```output
5
-1
```

## Low, high and mid

To track the part still in play, keep two positions: `low` and `high`. The middle is `(low + high) // 2`, which rounds down. If `nums[mid]` is less than the target, move `low` to `mid + 1`. If it is greater, move `high` to `mid - 1`.

The plus one and the minus one matter. The middle has already been checked, so skip it. If you wrote `low = mid` instead, the loop could run forever. When `low` passes `high`, nothing is left, and the target is not in the list.

## How fast is binary search

Halving a thousand items takes about ten steps. A million items take about twenty. That is O(log n). One catch: binary search only works on sorted data. On an unsorted list it gives wrong answers.

## The find function line by line

- Line 2 sets `low` to 0 and `high` to the last position.
- Line 3 loops while something is left.
- Line 4 finds the middle.
- Line 5 checks for a match, and line 6 returns its position.
- Line 7 asks if the middle is too small, so line 8 moves `low` up.
- Otherwise, line 10 moves `high` down.
- Line 11 returns -1, which means not found.
- Lines 15 and 16 search for 23, found at position 5, and for 7, which is missing.

## What you learned

- Binary search needs a sorted list.
- Check the middle and throw away half.
- Move `low` or `high` past the middle, never onto it.
- It takes about log n steps, even for a million items.

## Common questions

**Does binary search work on an unsorted list?** No. It assumes everything left of the middle is smaller and everything right is bigger. On unsorted data it can miss an item that is there. Sort first, or use `in`.

**Is there a built-in binary search in Python?** Yes. The `bisect` module in the standard library finds where a value belongs in a sorted list. `bisect.bisect_left(nums, 23)` gives 5 for the list above.

**Why `// 2` and not `/ 2`?** `//` rounds down to a whole number. A single `/` gives a float such as 3.0, and a float cannot be used as a list position.

**When is a plain `in` check better?** For a short list, or one you search only once. Sorting costs more than a single scan, so binary search pays off when you search the same sorted list many times.

**Can I write binary search with recursion?** Yes. The function calls itself on the left or right half, and the base case is an empty range. The loop version is usually shorter in Python.

Next in the series: sorting algorithms, and how to put a list in order.
