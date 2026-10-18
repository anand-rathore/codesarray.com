title: Python hash tables: how a dict finds a key so fast
summary: How a Python dict works inside: the key becomes a hash, the hash picks a slot, so lookup is O(1). Collisions, why a list cannot be a key, and how a set fits in.
description: Python hash tables explained: how a dict turns a key into a slot, what a collision is, and why a list is unhashable, with a small example and its real output.
date: 2026-10-18
read: 5 min read
lesson: 12
video: Python Hash Tables Explained | https://youtu.be/ekxk34cvUu8
image: cover.png
---
By the end of this page you will know how a Python dict finds a key without searching, what a collision is, and why a list can't be a dict key. It builds on [Python binary search](/articles/python/intermediate/binary-search/), which also finds things fast, but only in sorted data.

## What is a hash table in Python

A hash table is a way to store values so you can find one without looking at the others. A Python `dict` is a hash table, and so is a `set`. Both stay fast however much data they hold.

The example below is a toy version of the idea. It is not what Python really does, but it shows the steps.

```python
def slot(word, size):
    return sum(ord(c) for c in word) % size

for word in ["cat", "dog", "act"]:
    print(word, slot(word, 8))

ages = {"cat": 3, "dog": 5}
print(ages["dog"])
```

```output
cat 0
dog 2
act 0
5
```

## Hashing: from key to slot

A dict keeps a row of slots. To store a key, Python turns the key into a number, called its hash, and uses that number to pick a slot. Here, `slot("cat", 8)` adds up the letter codes (312) and takes the remainder by 8, which is 0. So `"cat"` and its value go in slot 0.

To look `"cat"` up later, Python does the same sum and jumps straight to slot 0. It never searches the other slots. That is why a dict lookup is O(1): the cost does not grow with the number of items.

## Collisions

Two different keys can land in the same slot. That is a collision. In the output above, `"cat"` and `"act"` both get slot 0, because they have the same letters and so the same sum.

Python does not lose either one. It checks whether the key already in the slot is the same key. If not, it probes on to another free slot and stores the new key there. With few collisions, lookups stay fast.

## Keys must be hashable

This only works if a key's hash never changes. So keys must be hashable. Strings, numbers and tuples of those are. A list can change, so its hash could change, and Python refuses:

```python
{[1, 2]: "x"}
```

```output
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
```

Two keys that are equal must also have the same hash. That is why `1` and `1.0` are one key in a dict: they are equal and hash alike. A `set` is the same machine with keys but no values.

## The code line by line

- Line 1 defines `slot`, which takes a word and the number of slots.
- Line 2 adds up the letter codes of the word and takes the remainder by `size`, so the answer is always a slot number.
- Line 4 loops over three words.
- Line 5 prints each word with its slot.
- Line 7 makes a real dict.
- Line 8 looks up `"dog"` directly and prints its value.

## What you learned

- A dict turns each key into a hash, and the hash picks a slot, so lookup is O(1).
- Keys that share a slot collide, and Python probes on to a free slot.
- Keys must be hashable, so a list can't be a key.

## Common questions

**Is Python's real hash function the letter sum?** No. That sum is only a toy. For strings, Python uses a much better mix, and it changes on every run: `hash("cat")` prints a different number each time you start Python, on purpose. The idea of hash, then slot, is the same.

**Can a tuple be a dict key?** Yes, if everything inside it is hashable. `{(1, 2): "x"}` works. `{(1, [2]): "x"}` raises `TypeError`, because the list inside is unhashable.

**Why does a dict slow down when it has many collisions?** Each collision means extra probing before the right key is found. Python keeps the table partly empty and grows it as it fills, so collisions stay rare and lookups stay close to O(1).

**How do I make my own class usable as a key?** Define `__eq__` and `__hash__` so that equal objects give the same hash. If you define `__eq__` alone, Python sets `__hash__` to `None` and the object is unhashable.

**Why does a set remove duplicates?** It stores each item by its hash, so a second equal item lands on the first one and is not added. `len({"a", "a", "b"})` is 2.

Next in the series: heaps and priority queues, and how to always get the smallest item first.
