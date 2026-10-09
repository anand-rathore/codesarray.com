title: Python dictionaries: keys, values, get, items and counting
summary: Store Python values by key in a dictionary, look them up, add new ones, loop over them with items(), avoid a KeyError with get(), and count words.
description: Python dictionaries for beginners: look up by key, add entries, avoid KeyError with get(), loop with items(), count words, and why lookup is O(1).
date: 2026-10-09
read: 4 min read
lesson: 7
video: Dictionaries | https://youtu.be/NNaw3jYEzwo
image: cover.png
---
A Python dictionary stores values by key, so you ask for something by name instead of by position. By the end of this page you will make a dictionary, look up and add entries, avoid a `KeyError` with `get()`, loop over every pair with `items()`, count how often words appear, and know why a lookup stays fast however big the dictionary gets.

## Keys and values

A dictionary holds pairs: a key and its value. `prices = {"apple": 3, "pear": 5}` has two entries. `prices["apple"]` gives `3`: you look up by key, not by position. Assigning to a new key, as in `prices["kiwi"] = 7`, adds an entry. Assigning to a key that already exists replaces its value.

## get, in and the KeyError

Ask for a key that is missing and Python raises an error: `prices["fig"]` gives `KeyError: 'fig'`. The safe way is `get()`. `prices.get("fig", 0)` returns the default, `0`, instead of crashing. If you leave the default out, `get()` returns `None`. The `in` test checks keys: `"pear" in prices` is `True`, and `3 in prices` is `False`, because `3` is a value, not a key.

## Looping with items

Call `items()` to get each key and value together. `for name, price in prices.items()` gives you every pair, in the order you added them. A key can be a string, a number or a tuple, but not a list, because a key must never change: `{[1, 2]: 5}` raises `TypeError: cannot use 'list' as a dict key (unhashable type: 'list')`.

```python
prices = {"apple": 3, "pear": 5}
print(prices["apple"])
prices["kiwi"] = 7
print(len(prices))
print(prices.get("fig", 0))

for name, price in prices.items():
    print(name, price)

words = ["py", "go", "py"]
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)
```

```output
3
3
0
apple 3
pear 5
kiwi 7
{'py': 2, 'go': 1}
```

Line 1 builds the dictionary and line 2 looks up `"apple"`. Line 3 adds `"kiwi"`, so line 4 prints `3` entries. Line 5 asks for `"fig"` with a default of `0`, and prints `0`. Lines 7 and 8 loop over every pair. Lines 10 to 14 count words: `counts` starts empty, and for each word `counts.get(w, 0) + 1` starts a new word at zero and adds one. The result is `py` twice and `go` once.

## Why lookup is fast

A dictionary turns the key into a number, called a hash, and jumps straight to that spot. So finding a key is O(1), even with a million entries. Looking for an item in a list checks the items one by one, which is O(n). That is also why keys must never change: if a key changed, its hash would point to the wrong spot.

## What you learned

- A dictionary maps keys to values, and `prices["apple"]` looks up by key.
- Assigning to a new key adds an entry; assigning to an existing key replaces its value.
- `get(key, default)` returns the default instead of raising a `KeyError`, and `in` checks keys.
- `items()` loops over keys and values together, in the order they were added.
- Lookup is O(1) because of hashing, and a list cannot be a key.

## Common questions

**How do I make an empty dictionary?** Use `{}` or `dict()`. Both give `{}`. Remember that an empty `{}` is a dictionary, not a set.

**How do I remove a key?** Use `del prices["pear"]`, or `prices.pop("pear")`, which also hands back the value. Both raise a `KeyError` if the key is missing.

**Are dictionaries ordered?** Yes. Since Python 3.7, a dictionary keeps the order in which you added its keys, so `list(prices)` is `['apple', 'pear', 'kiwi']`.

**Is there a shorter way to count?** Yes. `Counter("banana")` from `collections` gives `Counter({'a': 3, 'n': 2, 'b': 1})`. The `get()` loop above shows what it does underneath.

**Can two keys be the same?** No. A second assignment to the same key replaces the first value. Even `1` and `1.0` count as the same key, because they are equal.

This lesson follows on from [Python tuples and sets](/articles/python/beginner/tuples-and-sets/). Next in the series: functions.
