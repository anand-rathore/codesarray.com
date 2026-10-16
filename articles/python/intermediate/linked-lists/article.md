title: Python linked lists from scratch: Node class and head
summary: How a linked list works in Python: a Node class that holds a value and a link, the head, the None that ends the chain, how to walk it, and why adding at the front is O(1) but finding an item is not.
description: Python linked lists from scratch: build a Node class, link nodes from a head to None, walk the chain, and see why adding at the front is O(1).
date: 2026-10-16
read: 4 min read
lesson: 8
video: Python Linked Lists from Scratch | https://youtu.be/LV1J7lLj6zY
image: cover.png
---
By the end of this page you will be able to build a linked list in Python from a small class, walk it from the first node to the last, and explain why adding at the front is fast while finding an item is slow. It builds on [Python stacks and queues](/articles/python/intermediate/stacks-and-queues/) and [Python type hints](/articles/python/intermediate/type-hints/).

## What is a linked list in Python

A linked list is made of nodes. A node is a small box with two parts: it holds a value, and it holds a link to the next node. That link is just a reference, the same kind of reference a variable holds. Python has no built-in linked list type, so you build one from a class.

Here is the whole example. It is used for every section below.

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

head = Node("a", Node("b", Node("c")))

node = head
while node:
    print(node.value)
    node = node.next
```

```output
a
b
c
```

## How nodes link into a chain

Link nodes together and you get a chain. The first node is called the head. Each node points to the next one, and the last node points to `None`, which means the end. The list is only a variable, `head`, that holds the first node. Everything else is reached by following the links.

In the example, `Node("a", Node("b", Node("c")))` builds all three nodes in one expression. The innermost `Node("c")` has no second argument, so its `next` stays `None`. The `Node("b", ...)` node links to it, and the `Node("a", ...)` node links to that.

## Walk a linked list from the head

To read the list, start at the head and follow the links. Line 8 sets `node = head`. Line 9, `while node:`, keeps going while there is a node. A `Node` object is always truthy, and `None` is falsy, so the loop stops when the link is `None`. Line 10 prints the value. Line 11, `node = node.next`, moves to the next node.

That is why it prints `a`, then `b`, then `c`, one node at a time.

## Why add at the front of a linked list

Adding at the front is the strength of a linked list. Make a new node, and point it at the old head:

```python
head = Node("z", head)
```

Nothing else moves. That costs O(1). A Python list has to shift every item one place to the right to make room at the front with `insert(0, x)`, which costs O(n).

The trade is that a linked list has no index. There is no `items[2]`. To find the third item, you have to walk there from the head:

```python
head.next.next.value
```

Reaching an item by position costs O(n), because you follow one link for every step.

## What you learned

- A node holds a value and a link to the next node.
- The head is the first node, and the last node's link is `None`.
- To read the list, start at the head and follow `node.next` until you reach `None`.
- Adding at the front is O(1), but there is no index, so finding an item means walking the chain.

## Common questions

**Does Python have a built-in linked list?** No. The standard library has `collections.deque`, which is built from linked blocks, but you cannot walk its nodes yourself. When you need to see the nodes, as in this lesson, you write a `Node` class.

**Why is the argument called `next` when `next()` is a built-in?** `next` is also the name of the built-in function, and a parameter or attribute with that name hides it only inside that scope. It is the traditional name for the link, so the lesson uses it. If you ever need the built-in inside `__init__`, pick another name such as `next_node`.

**Is a linked list faster than a list?** Only for some jobs. Adding or removing at the front is O(1) for a linked list and O(n) for a list. Reading an item by position is O(1) for a list and O(n) for a linked list. For most Python code, a plain list or a `deque` is the better choice.

**What is a doubly linked list?** Each node also keeps a link to the previous node, so you can walk both ways. It costs one more reference per node. This lesson covers the singly linked list, where each node links only forward.

**What happens if a link points back to an earlier node?** The chain becomes a loop, and `while node:` never reaches `None`, so it runs forever. Keep each node's link pointing forward.

Next in the series: recursion, and how a function can call itself.
