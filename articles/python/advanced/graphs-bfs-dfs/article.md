title: Python graphs: BFS and DFS explained, with the shortest path
summary: How to store a graph in Python as an adjacency list, find the shortest path with breadth first search and a deque, and when depth first search is the better walk. One small function with its real output.
description: Python graphs, BFS and DFS explained: an adjacency list in a dict, breadth first search with a deque for the shortest path, and a seen set to stop loops.
date: 2026-10-20
read: 4 min read
lesson: 1
video: Python Graphs: BFS and DFS Explained | https://youtu.be/4WsKGZi4MUk
image: cover.png
---
By the end of this page you will know how to store a graph in Python, how to find the shortest path through it with breadth first search, and when to walk it depth first instead. It builds on [trees and traversal](/articles/python/intermediate/trees-and-traversal/), because a tree is just a graph with no loops.

## A graph is nodes joined by edges

A graph is a set of nodes joined by edges. In our example, A connects to B and C, B connects to D, and C connects to D. In Python you store it as a dictionary. Each key is a node, and its value is the list of its neighbours. That layout is called an adjacency list.

```python
graph = {"A": ["B", "C"], "B": ["D"],
         "C": ["D"], "D": []}
```

D has an empty list because no edge leaves it.

## Breadth first search finds the shortest path

Breadth first search, or BFS, goes level by level. It starts at A, which is zero steps away. Then it visits everything one step away, B and C. Then everything two steps away, D.

The first time you reach a node, you got there in the fewest steps. That is why BFS finds the shortest path. Two things make it work. A queue keeps the order, so older paths are tried first. A seen set stops you going in circles.

## Depth first search goes deep

Depth first search, or DFS, goes the other way. It follows one path as far as it can. From A it goes to B, then D. D is a dead end, so it backs up, and then tries C. Use it to explore everything, to find cycles, or to order tasks. It does not promise the shortest path.

## The code

This is breadth first search, with a start and a goal:

```python
from collections import deque

graph = {"A": ["B", "C"], "B": ["D"],
         "C": ["D"], "D": []}

def bfs(start, goal):
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        if path[-1] == goal:
            return path
        for nxt in graph[path[-1]]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(path + [nxt])

print(bfs("A", "D"))
```

Run it:

```output
['A', 'B', 'D']
```

Two steps, the shortest way from A to D.

## The code line by line

- Lines 3 and 4 are the graph, as an adjacency list.
- Line 6 defines `bfs` with a start and a goal.
- Line 7 makes a queue holding one path, just the start.
- Line 8 is the seen set.
- Line 9 loops while the queue still has paths.
- Line 10 takes the oldest path.
- Lines 11 and 12 return it if it ends at the goal.
- Line 13 loops over the neighbours of its last node.
- Lines 14 to 16 skip nodes already seen, mark new ones, and queue a longer path.
- Line 18 prints the answer.

## What you learned

- A graph is a dictionary of neighbour lists, called an adjacency list.
- BFS uses a queue, and the first path to reach the goal is the shortest.
- DFS goes deep first and explores everything, but does not promise the shortest path.
- A seen set stops a search going in circles.

## Common questions

**What if there is no path to the goal?** The queue runs empty, the loop ends, and the function returns `None`. Try `bfs("D", "A")` on this graph.

**Why use a deque and not a list?** `popleft()` on a deque takes the same time however long the queue is. `pop(0)` on a list has to shift every item along, so it slows down as the queue grows.

**Why do I need the seen set?** Without it, a graph with a loop never ends. With A pointing to B and B pointing back to A, a walk that does not remember where it has been keeps going until Python raises `RecursionError: maximum recursion depth exceeded`.

**How would I write DFS?** Call the function on each unseen neighbour:

```python
def dfs(node, seen):
    seen.add(node)
    print(node)
    for nxt in graph[node]:
        if nxt not in seen:
            dfs(nxt, seen)

dfs("A", set())
```

```output
A
B
D
C
```

It goes A, B, D, hits the dead end, backs up, and then visits C.

**Does DFS find the shortest path?** Not always. On a graph where A connects to B and D, B connects to C, and C connects to D, a DFS that takes the first neighbour first finds A, B, C, D. BFS finds A, D.

Next in the series: Dijkstra and weighted graphs, for when some edges cost more than others.
