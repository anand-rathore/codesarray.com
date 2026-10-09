title: Python negative indexing: get the last item with nums[-1]
summary: A negative index counts from the end of a Python list, so nums[-1] is always the last item, with no len() needed.
description: Python negative indexing: nums[-1] gives the last item of a list with no len() needed, nums[-2] the one before, and nums[-5] raises IndexError.
date: 2026-10-09
read: 2 min read
follows: 5
video: Negative indexing in Python | https://youtube.com/shorts/EeSZtH1598U
image: cover.png
---
To get the last item of a Python list, use negative indexing: `nums[-1]`. You do not need the length of the list, and it works however long the list is.

## Count back from the end

```python
nums = [10, 20, 30, 40]
print(nums[-1])
print(nums[-2])
print(nums[-4])
```

```output
40
30
10
```

Negative positions count from the end, starting at `-1`. So `nums[-1]` is the last item, `nums[-2]` is the one before it, and `nums[-4]` is the first item of this four-item list.

## What happens past the start

`nums[-5]` is one step too far for a list of four, so Python raises `IndexError: list index out of range`. The same error appears for any index that points outside the list.

## Things to know

- `nums[-1]` does the same job as `nums[len(nums) - 1]`, with less to type and less to get wrong.
- It works on strings and tuples too: `"abc"[-1]` is `'c'`.
- On an empty list, `[][-1]` raises `IndexError`, because there is no last item.

This is a short note on [Lists](/articles/python/beginner/lists/), lesson 5 of the Python beginner track.
