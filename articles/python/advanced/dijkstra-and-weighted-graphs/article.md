title: Python Dijkstra's algorithm with heapq: the cheapest path in a weighted graph
summary: How to find the cheapest path through a weighted graph in Python with Dijkstra's algorithm and heapq, how relaxation works, why a negative weight gives a wrong answer, and how Bellman-Ford fixes it. Two short functions with their real output.
description: Python Dijkstra's algorithm with heapq: find the cheapest path in a weighted graph, see relaxation traced by hand, and learn when negative weights break it.
date: 2026-10-20
read: 7 min read
lesson: 2
video: Python Dijkstra's Algorithm with heapq | https://youtu.be/q77VxBaM-zc
image: cover.png
---
By the end of this page you will know how to find the cheapest path through a weighted graph with Dijkstra's algorithm and `heapq`, what relaxation means, and when Dijkstra gives a wrong answer. It builds on [graphs, BFS and DFS](/articles/python/advanced/graphs-bfs-dfs/), and uses the heap from [heaps and priority queues](/articles/python/intermediate/heaps-and-priority-queues/).

## The fewest steps is not the cheapest route

Breadth first search finds the path with the fewest steps. That is the right answer when every step costs the same. Real roads do not. In a weighted graph every edge has a cost.

Take this graph: A to B costs 4, A to C costs 1, C to B costs 2, B to D costs 1, and C to D costs 5. Breadth first search picks A, B, D: two steps, but a total cost of 5. The cheapest route is A, C, B, D: three steps, but only 4 in total. Fewest steps is not the same as lowest cost.

In Python, each neighbour is now a pair: the node, and the weight of the edge to it.

```python
graph = {"A": [("B", 4), ("C", 1)],
         "B": [("D", 1)],
         "C": [("B", 2), ("D", 5)],
         "D": []}
```

## Dijkstra's idea

Keep the best distance you know so far to every node. Then always take the closest node you have not finished, and use it to look for shorter routes to its neighbours.

To find the closest one fast, keep the candidates in a heap. Python's `heapq` gives you the smallest item in O(log n). Each heap item is a pair, the distance first and then the node, so the smallest distance always comes out first.

## Relaxation, traced by hand

Run it on the graph above.

1. A is at distance 0. Its edges give B at 4 and C at 1.
2. C is the closest, so take C. From C, B costs 1 + 2 = 3. That beats 4, so update B. This update is called **relaxation**: you found a cheaper way, so you replace the old distance.
3. From C, D costs 1 + 5 = 6, so D is 6 for now.
4. The closest unfinished node is now B, at 3. From B, D costs 3 + 1 = 4. That beats 6, so relax D again.
5. D is last, and it is done.

The final distances: A is 0, C is 1, B is 3, and D is 4.

Why can you trust a finished node? Any other route to it must first pass through a node that is at least as far away, and adding a weight never makes a route shorter. That only holds when no weight is negative.

## A second example

S connects to A with weight 7 and to B with weight 2. B connects to A with weight 3 and to T with weight 8. A connects to T with weight 1.

Start at S. B is the closest, at 2. From B, A costs 5, which beats 7, so relax A. From B, T costs 10. Next A is the closest, at 5. From A, T costs 6, which beats 10, so relax T. The cheapest route from S to T is S, B, A, T, for a total of 6. Going straight through B to T would have cost 10.

## The code

```python
import heapq

graph = {"A": [("B", 4), ("C", 1)],
         "B": [("D", 1)],
         "C": [("B", 2), ("D", 5)],
         "D": []}

def dijkstra(start):
    dist = {start: 0}
    heap = [(0, start)]
    done = set()
    while heap:
        d, node = heapq.heappop(heap)
        if node in done:
            continue
        done.add(node)
        for nxt, w in graph[node]:
            nd = d + w
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return dist

print(dijkstra("A"))
```

Run it:

```output
{'A': 0, 'B': 3, 'C': 1, 'D': 4}
```

The same numbers as the trace.

## The code line by line

- Line 1 imports `heapq`.
- Lines 3 to 6 are the graph. Each node maps to a list of pairs: the neighbour and the weight.
- Line 8 defines `dijkstra` with a start.
- Line 9 is the distance dictionary, with the start at 0.
- Line 10 is the heap, holding one pair: distance 0 and the start node.
- Line 11 is the set of finished nodes.
- Line 12 loops while the heap has candidates.
- Line 13 pops the closest one, as a distance `d` and a node.
- Lines 14 and 15 skip a node that is already finished, because the heap can hold old, longer entries for it.
- Line 16 marks the node as finished.
- Line 17 loops over its neighbours, each with its weight.
- Line 18 is the new distance: `d` plus the weight.
- Line 19 asks whether that is better than the best known distance. A neighbour with no distance yet gets infinity from `dist.get`, so the answer is yes.
- Line 20 records the better distance. That is the relaxation.
- Line 21 pushes the neighbour onto the heap with its new distance.
- Line 22 returns the distances.
- Line 24 runs it from A.

## When Dijkstra gives a wrong answer

Dijkstra needs every weight to be zero or more. A negative weight breaks the rule that a finished node is final.

Take A to B costing 2, A to C costing 3, C to B costing -2, and B to D costing 1. Dijkstra finishes B at 2 and sets D to 3. Only later does it find that going through C reaches B at just 1. But B is already finished, so D is never fixed. Dijkstra says D is 3. The real cheapest route is A, C, B, D, which costs 2. It is a wrong answer with no error at all.

## Bellman-Ford handles negative weights

Bellman-Ford is slower but simpler. Start with every distance at infinity and the start at 0. Go through all the edges and relax each one. Repeat that once for every node, minus one. After that, every shortest path has been found. Then do one more pass: if anything still improves, there is a negative cycle, a loop that gets cheaper every time round, so no cheapest route exists.

The cost is O(V x E), against O(E log V) for Dijkstra.

```python
edges = [("A", "B", 2), ("A", "C", 3),
         ("C", "B", -2), ("B", "D", 1)]

def bellman_ford(start, nodes):
    dist = {n: float("inf") for n in nodes}
    dist[start] = 0
    for _ in range(len(nodes) - 1):
        for a, b, w in edges:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
    for a, b, w in edges:
        if dist[a] + w < dist[b]:
            raise ValueError("negative cycle")
    return dist

print(bellman_ford("A", "ABCD"))
```

Run it:

```output
{'A': 0, 'B': 1, 'C': 3, 'D': 2}
```

D is 2, the right answer, where Dijkstra said 3.

- Lines 1 and 2 are the edge list, as triples: from, to and weight.
- Line 4 defines the function with a start and the nodes.
- Line 5 sets every distance to infinity, and line 6 sets the start to 0.
- Line 7 repeats the pass once fewer than the number of nodes.
- Lines 8 to 10 go through every edge and relax it.
- Lines 11 to 13 are the extra pass: if anything still improves, raise an error for a negative cycle.
- Line 14 returns the distances.

## What you learned

- With weights, the fewest steps is the wrong question; you want the lowest total cost.
- Dijkstra always finishes the closest node, and `heapq` finds it fast.
- Relaxation replaces a distance when you find a cheaper way.
- Dijkstra runs in O(E log V), but only when no weight is negative.
- With negative weights, use Bellman-Ford.

## Common questions

**What if a node cannot be reached from the start?** It never gets a distance, so it does not appear in the dictionary. `dijkstra("A")` on a graph where `"B"` has no edge from A simply has no `"B"` key.

**Why push a tuple like `(nd, nxt)`?** Python compares tuples one item at a time, so the distance decides the order. If two distances tie, it compares the node names, which works for strings.

**Why can the heap hold old entries?** When you relax a node, you push its new, shorter distance, but the old, longer entry is still in the heap. The `done` check on lines 14 and 15 throws the old one away when it comes out.

**How do I get the route and not only the cost?** Keep a second dictionary that records which node you came from each time you relax a distance, then walk it backwards from the goal.

**Does a zero weight work?** Yes. Dijkstra needs weights of zero or more, not only positive ones.

Next in the series: dynamic programming, solving a big problem from small ones you already solved.
