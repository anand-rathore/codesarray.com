title: Python trees and traversal: binary trees and in-order walk
summary: How a Python binary tree is built from nodes, what makes it a search tree, and how an in-order walk visits every node in sorted order. A small recursive function with its real output.
description: Python trees and traversal explained: build a binary tree from nodes, learn the search tree rule, and walk it in order with recursion, with real output.
date: 2026-10-19
read: 5 min read
lesson: 14
video: Python Trees and Traversal: Binary Trees, In-Order Walk | https://youtu.be/ZYZUSZJeNa4
image: cover.png
---
By the end of this page you will know how a tree is built from nodes in Python, what makes a binary tree a search tree, and how to visit every node in order with a short recursive function. It builds on [Python heaps and priority queues](/articles/python/intermediate/heaps-and-priority-queues/), which are trees stored inside a list, and on [Python recursion](/articles/python/intermediate/recursion/), which the walk uses.

## What is a tree in Python

A tree is made of nodes. Each node holds a value and points to at most two children, a left one and a right one. A tree like this is called a binary tree. The top node is the root, and a node with no children is a leaf.

In our example the root is 4. Its left child is 2, which has two children of its own, 1 and 3. Its right child is 6. The nodes 1, 3 and 6 are leaves.

## Binary search trees

A binary search tree adds one rule: smaller values go left, and bigger values go right. Look at 2. On its left sits 1, which is smaller. On its right sits 3, which is bigger. The rule holds at every node, so everything left of 4 is smaller than 4, and everything right of it is bigger.

That rule makes searching quick. At each step you go left or right and skip a whole side of the tree. To find 3, start at 4, go left to 2, go right to 3, and never look at 6.

## The in-order walk

To visit every node you walk the tree. An in-order walk does the left side first, then the node, then the right side. Start at 4, go left to 2, go left to 1. Nothing is on the left of 1, so visit 1. Back up to 2, visit 2. Then its right side, 3. Back to 4, visit 4. Then 6.

The values come out 1, 2, 3, 4, 6. They are sorted, without a sort. In a binary search tree an in-order walk always gives sorted order.

## Other walk orders

There are other orders. A pre-order walk visits the node before its sides, and a post-order walk visits it after. Both go deep first. A breadth-first walk goes level by level instead.

## The code

```python
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def inorder(node):
    if node:
        inorder(node.left)
        print(node.value)
        inorder(node.right)

root = Node(4, Node(2, Node(1), Node(3)), Node(6))
inorder(root)
```

```output
1
2
3
4
6
```

## The code line by line

- Lines 1 to 5 make a node. It holds a value, and a left and a right child, which are empty by default.
- Line 7 defines `inorder`.
- Line 8 stops when the node is empty, so a missing child ends the walk down that side.
- Line 9 walks the left side.
- Line 10 prints the value.
- Line 11 walks the right side.
- Line 13 builds our tree.
- Line 14 starts the walk at the root.

## What you learned

- A tree is nodes with a left and a right child; the top is the root and a node with no children is a leaf.
- In a binary search tree, smaller goes left and bigger goes right.
- An in-order walk does left, node, right, and visits the values sorted.
- Pre-order, post-order and breadth-first are other ways to walk.

## Common questions

**What do pre-order and post-order print for this tree?** Move the `print` line. Pre-order, with the print before the two calls, gives 4, 2, 1, 3, 6. Post-order, with the print after them, gives 1, 3, 2, 6, 4.

**What is a breadth-first walk?** It visits the tree level by level: 4, then 2 and 6, then 1 and 3. You use a queue instead of recursion. Start with the root in a `deque`, then repeatedly `popleft` a node, record its value and append its children. For this tree the order is `[4, 2, 6, 1, 3]`.

**Is an in-order walk always sorted?** Only for a binary search tree. In any other binary tree it still visits left, node, right, but the values can come out in any order.

**Why does `inorder` check `if node`?** Without it, the walk would call `inorder(None)` on a leaf's missing child and Python would raise `AttributeError: 'NoneType' object has no attribute 'left'`. The check is the base case that stops the recursion.

**Can the walk run out of stack space?** Yes. A tree that is one long chain, about 2,000 nodes deep, makes `inorder` raise `RecursionError: maximum recursion depth exceeded`, because Python stops at about 1,000 nested calls. Balanced trees are far shallower.

Next in the series: HTTP and JSON APIs, and how to talk to the web.
