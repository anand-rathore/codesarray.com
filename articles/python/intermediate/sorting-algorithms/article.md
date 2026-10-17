title: Python sorting algorithms: bubble sort, merge sort, sorted()
summary: How sorting works in Python: bubble sort swaps neighbours in O(n squared), merge sort splits and merges in O(n log n), and sorted() with key does the job for you in real code.
description: Python sorting algorithms explained: write bubble sort, see why merge sort is faster, and use sorted() and key= for real work, with real output.
date: 2026-10-17
read: 4 min read
lesson: 11
video: Python Sorting Algorithms Explained | https://youtu.be/8SOdHPZWif0
image: cover.png
---
By the end of this page you will be able to write bubble sort in Python, explain why merge sort is so much faster, and know what `sorted()` does when you call it. It builds on [Python binary search](/articles/python/intermediate/binary-search/), which needs a sorted list to work.

## What are sorting algorithms in Python

A sorting algorithm is a set of steps that puts a list in order. Two are worth knowing by name: bubble sort, because it is the simplest, and merge sort, because it shows how to do better. In real code you will not write either. Python's built-in `sorted()` does the job.

Here is the example used for the rest of the page.

```python
def bubble_sort(nums):
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, len(nums)):
            if nums[i - 1] > nums[i]:
                nums[i - 1], nums[i] = nums[i], nums[i - 1]
                swapped = True


nums = [5, 2, 8, 1]
bubble_sort(nums)
print(nums)
print(sorted(["fig", "apple", "kiwi"], key=len))
```

```output
[1, 2, 5, 8]
['fig', 'kiwi', 'apple']
```

## Bubble sort

Look at two neighbours. If the left one is bigger, swap them. Walk down the list doing that, and the biggest item bubbles to the end. Repeat until a pass makes no swaps.

It is simple, but every pass walks the whole list, and you need about n passes. That is O(n squared). Fine for four items, slow for a hundred thousand.

## Merge sort

Merge sort is smarter. Split the list in half, again and again, until every piece has one item. A single item is already sorted. Then merge the pieces back together: compare the front of two sorted pieces, and take the smaller one each time.

Halving gives about log n levels, and each level does n work. So merge sort is O(n log n), far faster than O(n squared).

## Python's sorted and Timsort

`sorted()` uses Timsort, a fast mix of merge sort and insertion sort. It is O(n log n), and it is stable, so equal items keep their order. To sort by something other than the item itself, pass `key`. For example, `key=len` sorts words by length.

## The code line by line

- Line 2 starts `swapped` as `True`.
- Line 3 loops while a swap happened.
- Line 4 resets `swapped` to `False`.
- Line 5 walks each neighbouring pair.
- Line 6 asks if the left one is bigger.
- Line 7 swaps them in one line, and line 8 records that a swap happened.
- Lines 11 to 13 sort four numbers and print them.
- Line 14 uses `sorted()` with `key=len` on three words.

## What you learned

- Bubble sort swaps neighbours, and is O(n squared).
- Merge sort splits and merges, and is O(n log n).
- In real code, use `sorted()`, with `key` to choose what to sort by.

## Common questions

**What is the difference between `sorted()` and `list.sort()`?** `sorted(nums)` returns a new list and leaves `nums` alone. `nums.sort()` changes the list in place and returns `None`, so `x = nums.sort()` makes `x` equal to `None`.

**How do I sort from biggest to smallest?** Pass `reverse=True`. `sorted([5, 2, 8, 1], reverse=True)` gives `[8, 5, 2, 1]`.

**What does stable mean?** Items that compare equal keep their original order. Sorting `[("b", 2), ("a", 2), ("c", 1)]` by the second value gives `("c", 1)` first, then `("b", 2)` and `("a", 2)` in the order they started.

**How do I sort text without caring about capital letters?** Use `key=str.lower`. A plain `sorted(["Bob", "alice", "Carl"])` puts `alice` last, because capitals sort first. With `key=str.lower` you get `['alice', 'Bob', 'Carl']`.

**Why learn bubble sort if nobody uses it?** It shows what sorting means one step at a time, and why O(n squared) gets slow. Merge sort then shows how splitting the problem fixes that.

Next in the series: hash tables, and how a dict finds things so fast.
