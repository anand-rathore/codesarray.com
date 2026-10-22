title: Python trie and union find: prefix search, autocomplete and Kruskal
summary: How to build a trie in Python for prefix search and autocomplete, then union find with path compression and union by size, and use it to run Kruskal's algorithm for a minimum spanning tree. Four short programs with their real output.
description: Python trie and union find explained: prefix search and autocomplete with a nested dict, union find with path compression, and Kruskal's algorithm, with runnable code.
date: 2026-10-22
read: 10 min read
lesson: 4
video: Tries and Union Find in Python | https://youtu.be/P68ArT9qyMw
image: cover.png
---
By the end of this page you will be able to build a Python trie that answers "which words start with these letters?", build a union find that answers "are these two things in the same group?", and use union find to run Kruskal's algorithm for the cheapest way to connect a graph. It builds on [hash tables](/articles/python/intermediate/hash-tables/), [trees](/articles/python/intermediate/trees-and-traversal/) and [graphs, BFS and DFS](/articles/python/advanced/graphs-bfs-dfs/).

## What a trie is, and why prefix search is fast

You have a list of words and a user types `ca`. You want every word that starts with `ca`. With a plain list you check every word, and the work grows with the size of the list. A trie (the name comes from "retrieval") fixes that by sharing letters. Each letter is one step down a tree, and words that begin the same way share the same first steps.

Take `car`, `card`, `care`, `cat` and `dog`. The root has two branches, `c` and `d`. Under `c` comes `a`. Under `a` come `r` and `t`. Under `r` come `d` and `e`. `car`, `card` and `care` all share the path `c`, `a`, `r` and only split at the end. The question "which words start with `ca`" is now a walk: follow `c`, then `a`, and everything below that point is the answer.

## The end marker: a word or only a prefix

`car` is a word, and it is also the start of `card`. To tell them apart, put an end marker on the node. In the code it is the key `"$"`. The node for `c`, `a`, `r` gets a `"$"` to say a word ends here, and it still has children for `d` and `e`.

Three lookups show the difference. `has("car")` walks `c`, `a`, `r` and finds the `"$"`, so it is a word. `has("ca")` walks `c`, `a`: the node exists but has no `"$"`, so `ca` is a prefix and not a word. `cow` walks `c`, then finds no branch for `o` and stops at once. A lookup costs the length of the word, O(L), whether the trie holds ten words or ten million. A set can tell you whether a whole word exists, but it cannot answer a prefix question without scanning every word. The price of a trie is memory, since every letter is a node.

## A trie in Python

```python
class Trie:
    def __init__(self):
        self.root = {}

    def add(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def find(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def has(self, word):
        node = self.find(word)
        return node is not None and "$" in node

words = Trie()
for w in ["car", "card", "care", "cat", "dog"]:
    words.add(w)

print(words.has("car"))
print(words.has("ca"))
print(words.find("ca") is not None)
print(words.find("cow") is not None)
```

```output
True
False
True
False
```

Each node is a dictionary that maps a letter to the node below it. In `add`, `setdefault` returns the child for this letter and creates an empty one if there is none, so the loop walks down and builds as it goes, then puts the `"$"` marker on the last node. `find` walks a prefix and returns the node it reaches, or `None` if a letter has no branch. `has` finds the node and checks the marker is there. The four answers are `True`, `False` (only a prefix), `True` (the prefix exists) and `False` (no branch for `o`). This trie is for lowercase letters; a word containing `"$"` would clash with the marker.

## Autocomplete with a trie

A search box needs more than yes or no: it needs every word below the prefix. Walk the prefix, then collect everything under that node with a stack.

```python
root = {}
for word in ["car", "card", "care", "cat", "dog"]:
    node = root
    for ch in word:
        node = node.setdefault(ch, {})
    node["$"] = True

def complete(prefix):
    node = root
    for ch in prefix:
        if ch not in node:
            return []
        node = node[ch]
    found, stack = [], [(node, prefix)]
    while stack:
        node, text = stack.pop()
        for ch, child in node.items():
            if ch == "$":
                found.append(text)
            else:
                stack.append((child, text + ch))
    return sorted(found)

print(complete("car"))
print(complete("x"))
```

```output
['car', 'card', 'care']
[]
```

The first loop in `complete` returns an empty list if the prefix is not in the trie. Then `found` collects words and `stack` holds `(node, text so far)` pairs. Each pop looks at the node's children: the `"$"` key means the text is a word, and any other child is pushed with one more letter. It is a depth first walk of everything below the prefix, and `sorted` puts the words in order.

## Union find: are these in the same group?

Six people are numbered 0 to 5, and you hear facts like "0 knows 1", "2 knows 3", "1 knows 3". Are 0 and 3 in the same circle of friends? Union find keeps a set of groups and supports two moves: `find` tells you which group a person belongs to, and `union` merges two groups.

Each group is a tree and every person keeps one pointer, to a parent. The person at the top points to themselves and is the root, and the root is the name of the group. Start with six groups, everyone pointing to themselves. `union(0, 1)` makes 1 point to 0. `union(2, 3)` makes 3 point to 2. `union(1, 3)` finds the roots, 0 and 2, which differ, so one root is attached under the other. Now 0 and 3 have the same root, so they are in the same group, while 5 is still its own root.

## Path compression and union by size

If groups are attached carelessly, trees can grow into long chains and a `find` has to climb the whole chain. Two ideas fix that. Path compression: when `find` climbs to the root, make every person on the way point straight at the root, so the next `find` takes one step. Union by size: when two groups merge, hang the smaller one under the bigger one so trees stay shallow. Together they make each operation almost constant time, O(alpha of n), where alpha is the inverse Ackermann function, which never goes above 5 for any input that fits in a computer. In practice, treat it as O(1).

```python
parent = list(range(6))
size = [1] * 6

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True

union(0, 1)
union(2, 3)
union(1, 3)
print(find(0) == find(3))
print(find(0) == find(5))
print(union(0, 2))
print(parent)
```

```output
True
False
False
[0, 0, 0, 0, 4, 5]
```

`parent[i]` starts as `i`, so everyone is their own root, and `size` tracks how big each group is. `find` is three lines: if `x` is not its own parent, set its parent to the `find` of its parent, then return it. The pointers are fixed as the recursion unwinds. `union` finds both roots, returns `False` if they are equal (already together), swaps so `ra` is the bigger group, hangs `rb` under it and adds the sizes. The output says 0 and 3 are together, 0 and 5 are not, and a second `union(0, 2)` changes nothing. In the final list, 3 points to 0, not to 2: path compression already pointed it straight at the root.

## Kruskal's algorithm: the cheapest way to connect everything

Four cities, and a cost for laying a cable between some pairs. The cheapest set of edges that connects all of them with no cycle is a minimum spanning tree. Kruskal's idea is greedy, and here greedy is correct: sort the edges from cheapest to most expensive, and for each one ask union find whether its two ends are already connected. If not, take the edge and union them. If they are, skip it, because it would make a cycle.

```python
def kruskal(n, edges):
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    total, chosen = 0, []
    for w, a, b in sorted(edges):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            total += w
            chosen.append((a, b))
    return total, chosen

edges = [(4, 0, 1), (1, 0, 2), (3, 1, 2), (2, 1, 3), (5, 2, 3)]
print(kruskal(4, edges))
print(kruskal(1, []))
```

```output
(6, [(0, 2), (1, 3), (1, 2)])
(0, [])
```

Each edge is a `(weight, a, b)` tuple, so `sorted(edges)` sorts by weight first. The edges in order cost 1 (0 to 2), 2 (1 to 3), 3 (1 to 2), 4 (0 to 1) and 5 (2 to 3). Kruskal takes 0 to 2, takes 1 to 3, and takes 1 to 2, which joins the two groups. Then 0 to 1 and 2 to 3 are skipped, since their ends are already connected. That is three edges with a total cost of 6, and a spanning tree of n nodes always has n minus 1 edges. The sort dominates the time, so it is O(E log E). One node and no edges gives `(0, [])`. If the graph is not connected, the result is a cheapest forest, one tree for each piece.

## What you learned

- A trie stores words letter by letter, so words with a shared start share a path, and a lookup or prefix check costs the length of the word.
- An end marker (`"$"`) tells a word from a prefix.
- Union find keeps groups as trees of parent pointers: `find` returns the root, `union` merges two groups.
- Path compression and union by size make both operations almost constant time.
- Kruskal sorts the edges and takes each one that joins two different groups.

## Common questions

**When should I use a trie instead of a set?** Use a set to ask whether a whole word exists. Use a trie when you need prefix questions, such as autocomplete, because a set would have to scan every word.

**Why does `has("ca")` return `False` when the prefix exists?** `has` checks the `"$"` marker. `ca` is a path in the trie but no word ends there, so it is only a prefix. `find("ca")` returns the node.

**What happens if two people are already in the same group?** `union` finds equal roots and returns `False` without changing anything, which is exactly the cycle check Kruskal uses.

**Do I need both path compression and union by size?** Either one helps on its own, and together they give near constant time. The code above uses both.

**Does Kruskal work on a graph that is not connected?** It still runs, and returns a minimum spanning forest: one cheapest tree for each connected piece.

Next in the series: asyncio, running many waits at the same time.
