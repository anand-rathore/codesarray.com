title: Python memory management: reference counting, garbage collection and __slots__
summary: How Python frees memory: reference counting with sys.getrefcount, reference cycles and the gc module, why sys.getsizeof is shallow and tracemalloc is not, what __slots__ saves, how small integers and interned strings are shared, and how weakref works. Four short programs with their real output.
description: Python memory management explained: reference counting, reference cycles, gc.collect(), tracemalloc, __slots__ and weakref, with runnable code and real output.
date: 2026-10-24
read: 8 min read
lesson: 7
video: Python memory management: refcounting, GC and __slots__ | https://youtu.be/CitFW-NA454
image: cover.png
---
By the end of this page you will know how Python manages memory: how it frees an object the moment nothing needs it, why two objects that point at each other need a second tool, how to measure the real size of your data, and three ways to work with memory on purpose: `__slots__`, shared objects and weak references. It follows [threads, processes and free threading](/articles/python/advanced/threads-processes-free-threading/).

## Reference counting

You never call `free` in Python. Every object carries a number: how many references point at it. A reference is a name, a list slot, an attribute, anything that holds the object. When the number reaches zero, nobody can use the object any more, so Python frees it at once.

```python
import sys


class Node:
    def __init__(self, name):
        self.name = name

    def __del__(self):
        print("freed", self.name)


a = Node("a")
print(sys.getrefcount(a))
b = a
print(sys.getrefcount(a))
del b
print(sys.getrefcount(a))
del a
print("done")
```

`__del__` runs just before an object is freed, so it shows us the moment. `sys.getrefcount(a)` reports one more than you might expect, because passing `a` into the call is itself a reference. The program prints:

```output
2
3
2
freed a
done
```

One name gives 2 (one real reference plus the call). `b = a` copies nothing, it adds a second name for the same object, so 3. `del b` removes a name and takes it back to 2. `del a` takes it to zero, and `freed a` prints on that very line, before `done`. This is why Python usually frees things so promptly.

## Reference cycles

Counting has one blind spot. If object x points at y and y points back at x, each keeps the other's count at 1, even after your own names are gone. Nothing can reach them, yet neither count ever reaches zero, so counting alone never frees them.

The second tool is the cyclic garbage collector, in the `gc` module. It does not count. It looks: it follows references from the names your program can still reach, and anything it cannot get to is garbage, even if it is holding on to something else.

```python
import gc


class Node:
    def __init__(self, name):
        self.name = name
        self.other = None

    def __del__(self):
        print("freed", self.name)


x = Node("x")
y = Node("y")
x.other = y
y.other = x
del x, y
print("deleted")
print(gc.collect())
print(gc.get_threshold())
```

```output
deleted
freed x
freed y
2
(2000, 10, 10)
```

After `del x, y` nothing prints: the cycle is still alive. `gc.collect()` finds the pair, frees both, and returns 2, the number of objects it freed. The collector also runs by itself, so you rarely call it.

Checking everything all the time would be slow, so the collector sorts objects into three generations. New objects start in generation 0, which is checked often. Survivors move to generation 1 and then generation 2, which are checked rarely, because an object that has lived this long usually keeps living. `gc.get_threshold()` shows the settings: `(2000, 10, 10)`.

One version note. Python 3.14.0 shipped an incremental collector, and it was taken out again in 3.14.5. Teach and rely on the generational collector described here.

## How big is an object?

`sys.getsizeof` gives the size of one object in bytes. An empty list is 56 bytes, a list of three numbers is 88, and a list of a hundred items is 856, about eight bytes per item because the list stores a pointer for each. An integer is 28 bytes and a one-letter string is 42.

Note the word shallow. `getsizeof` counts the object itself, not what it points to. A list holding one list of three numbers and a list holding one list of nine numbers both report 64 bytes. To find the real cost, measure with `tracemalloc`, which watches the memory your program actually allocates.

## __slots__

By default every instance of your class carries a dictionary, so you can add any attribute at any time. That freedom costs memory, and with 100,000 small objects it adds up. If you know the attributes in advance, write `__slots__` with their names and Python stores them in a fixed layout, with no dictionary per object.

```python
import tracemalloc


class Plain:
    def __init__(self):
        self.x, self.y = 1, 2


class Slim:
    __slots__ = ("x", "y")

    def __init__(self):
        self.x, self.y = 1, 2


def measure(cls):
    tracemalloc.start()
    items = [cls() for _ in range(100_000)]
    size, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return size // 1_000_000


print(measure(Plain), measure(Slim))
```

```output
9 5
```

`measure` builds 100,000 objects and asks `tracemalloc` how many bytes are in use, in megabytes. The plain class takes 9 MB and the slotted one 5 MB, almost half. The numbers vary a little by version, but the gap stays. The trade is that the freedom is gone: setting an attribute that is not in `__slots__` raises an `AttributeError`. Dataclasses can do this for you with `slots=True`.

## Shared objects and weak references

Python keeps one shared copy of the small integers from -5 up to 256, and of strings that look like names in your source code. Strings built while the program runs are not shared unless you call `sys.intern`. The last tool, `weakref`, lets you refer to an object without keeping it alive, which is what a cache wants.

```python
import sys
import weakref


class Big:
    pass


a = int("256")
b = int("256")
print(a is b)
c = int("257")
d = int("257")
print(c is d)
s = "".join(["py", "thon"])
t = "".join(["py", "thon"])
print(s is t, sys.intern(s) is sys.intern(t))

big = Big()
ref = weakref.ref(big)
print(ref() is big)
del big
print(ref())
```

```output
True
False
False True
True
None
```

`int("256")` twice gives the very same object, so `is` says `True`. `int("257")` twice gives two objects with equal values, so `is` says `False`. The two strings were built at run time, so they are different objects until `sys.intern` makes them one. The lesson: compare values with `==` and keep `is` for `None`.

A weak reference does not count. `ref()` returns the object while it is alive, and `None` once it has been freed, as the last line shows. `weakref.WeakValueDictionary` is a dictionary whose entries vanish on their own when the value is freed. Your own classes support weak references, but plain lists, dicts and numbers do not.

## What you learned

- Every object counts its references and is freed the moment the count reaches zero.
- A reference cycle keeps its own counts above zero, so the garbage collector in `gc` finds it, using generations.
- `sys.getsizeof` is shallow; use `tracemalloc` to measure for real.
- `__slots__` removes the per-object dictionary: 9 MB down to 5 MB for 100,000 objects.
- Small integers and interned strings are shared, so compare values with `==`.
- A weak reference points at an object without keeping it alive.

## Common questions

**Does Python have a garbage collector?** Yes, two parts. Reference counting frees most objects the instant they are unused, and the cyclic garbage collector in `gc` frees groups of objects that only point at each other.

**Do I need to call gc.collect()?** Almost never. The collector runs by itself. Calling it is useful in tests and demos, as above, where you want to see a cycle freed on purpose.

**Why does sys.getrefcount show one extra?** Passing the object to the function creates a temporary reference for the duration of the call.

**Why is sys.getsizeof wrong for my data?** It is not wrong, it is shallow: it counts only the container. Use `tracemalloc` for the whole cost.

**When should I use __slots__?** When you make very many small objects with a fixed set of attributes. For a handful of objects the saving is not worth losing the flexibility. Next in the series are descriptors and metaclasses, which is how `__slots__` itself is built.
