title: Python dynamic programming: memoisation, tabulation and lru_cache
summary: How dynamic programming works in Python: why recursive Fibonacci repeats work, memoisation with lru_cache, tabulation with a table, then 0/1 knapsack, the longest increasing subsequence and edit distance, each with real output.
description: Python dynamic programming explained: memoisation with lru_cache vs tabulation, then knapsack, longest increasing subsequence and edit distance with runnable code.
date: 2026-10-22
read: 6 min read
lesson: 3
video: Dynamic Programming in Python | https://youtu.be/9N1-3CjQSEs
image: cover.png
---
By the end of this page you will know how dynamic programming works in Python: why some recursive functions repeat work, the two fixes (memoisation and tabulation), and how the same idea solves knapsack, the longest increasing subsequence and edit distance. It builds on [recursion](/articles/python/intermediate/recursion/) and on [graphs, BFS and DFS](/articles/python/advanced/graphs-bfs-dfs/).

## Why recursive Fibonacci repeats work

Each Fibonacci number is the sum of the two before it, so `fib(5)` is `fib(4) + fib(3)`. As a plain recursive function that is short, but `fib(4)` calls `fib(3)` again, and `fib(3)` is worked out twice. For `fib(5)` the function is called 15 times, and every call splits in two, so the work roughly doubles with each step: about O(2 to the n). `fib(50)` would take hours.

Dynamic programming applies when a problem has two properties. It breaks into smaller subproblems of the same kind, and those subproblems overlap, so the same one comes up many times. The fix is to solve each subproblem once and remember the answer.

## Memoisation: recursion with a notebook

Memoisation is top down. Keep the recursive function and add a notebook: look the answer up first, and only compute it if it is missing. Python gives you the notebook as `lru_cache` from `functools`. With `maxsize=None` it never forgets. The arguments must be hashable because they are the keys, so numbers, strings and tuples work and a list raises `TypeError: unhashable type: 'list'`.

With the cache, `fib(5)` does 6 real computations instead of 15, and `fib(50)` does 51.

## Tabulation: fill a table from the bottom

Tabulation is bottom up, with no recursion. Make a table, fill in the smallest answers first, and build up: 0, 1, then each cell is the sum of the two before it. The answer is the last cell. Finding an order where every cell's inputs are already filled is the whole trick.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def fib_table(n):
    table = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]

print(fib(50))
print(fib_table(50))
print(fib.cache_info().misses)
```

```output
12586269025
12586269025
51
```

Line 3 is the whole of memoisation. Lines 9 to 13 are the table version, and `fib.cache_info().misses` on the last line counts the real computations: 51, one for each value from 0 to 50. Both versions work for n of zero or more.

Which should you use? Memoisation is easier to write because you start from the recursive idea, and it only solves the subproblems you need. Tabulation is usually a little faster and has no recursion limit. Python stops at about 1,000 nested calls, so a memoised `fib(5000)` raises `RecursionError`, while a table handles it and returns a number with 1,045 digits.

## 0/1 knapsack: take it or skip it

A bag holds a weight of 7. The items weigh 1, 3, 4 and 5 and are worth 1, 4, 5 and 7. A greedy choice takes the weight 5 item and the weight 1 item for a value of 8. But weights 3 and 4 fit exactly and are worth 9, so we have to try the choices.

Let `best[c]` be the most value you can carry with capacity `c`. For each item and each capacity you either skip the item, keeping `best[c]`, or take it, which gives its value plus `best[c - w]`. Keep the larger.

```python
def knapsack(weights, values, capacity):
    best = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]

print(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7))
```

```output
9
```

The capacities loop from high to low, so each item is used at most once. The time is O(items times capacity).

## Longest increasing subsequence

Find the longest run that goes up, in order, where the numbers do not have to be next to each other. Let `best[i]` be the length of the longest run that ends at position `i`. Every number alone is a run of 1. For each earlier number that is smaller, `x` can extend its run.

```python
def lis(nums):
    best = [1] * len(nums)
    for i, x in enumerate(nums):
        for j in range(i):
            if nums[j] < x:
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)

print(lis([10, 9, 2, 5, 3, 7, 101, 18]))
```

```output
4
```

The run is 2, 3, 7, 101. Two loops make it O(n squared). The `default=0` covers an empty list.

## Edit distance

Edit distance is the fewest single-letter edits (insert, delete, replace) that turn one word into another. `d[i][j]` is the distance between the first `i` letters of one word and the first `j` of the other. The first row and column are easy: turning `i` letters into nothing takes `i` deletes. Every other cell is the smallest of three neighbours: the cell above plus 1 (delete), the cell on the left plus 1 (insert), and the diagonal plus 1 if the letters differ or plus 0 if they match.

```python
def edit_distance(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i, x in enumerate(a, 1):
        for j, y in enumerate(b, 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + (x != y))
    return d[-1][-1]

print(edit_distance("kitten", "sitting"))
```

```output
3
```

Replace k with s, replace e with i, insert g. The table has m times n cells, so the time is O(m times n).

## What you learned

- Dynamic programming solves each overlapping subproblem once.
- Memoisation is top down: recursion plus a cache, and `lru_cache` does it in one line.
- Tabulation is bottom up: a loop that fills a table, with no recursion limit.
- Knapsack asks, take the item or skip it, looping capacities downward.
- The longest increasing subsequence and edit distance fill a table from earlier cells.

## Common questions

**How do I know a problem needs dynamic programming?** Check that it splits into smaller problems of the same kind and that the same small problems come up again and again. If they never repeat, plain recursion is enough.

**Does `lru_cache` work with a list argument?** No. The arguments become dictionary keys, so they must be hashable. Pass a tuple instead.

**Why does a memoised `fib(5000)` fail?** Each call waits for the one below it, and Python limits nested calls to about 1,000, so it raises `RecursionError`. A table has no recursion and works.

**Why loop the knapsack capacities downward?** So each item is used once. Looping upward would let the same item be counted again in the same pass.

**Does edit distance work on an empty word?** Yes. `edit_distance("", "abc")` is 3, three inserts, and two empty words give 0.

Next in the series: tries and union find, two structures for prefixes and for groups.
