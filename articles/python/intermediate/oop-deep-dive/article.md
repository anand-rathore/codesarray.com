title: Python classes explained: dunder methods, property and super
summary: How a Python class prints itself with dunder methods, hides a function behind an attribute with @property, builds objects with @classmethod, and extends a parent class with super().
description: Python classes explained: dunder methods like __repr__, @property, classmethod vs staticmethod, inheritance and super().__init__, with one runnable example.
date: 2026-10-16
read: 4 min read
lesson: 5
video: Python Classes Explained | https://youtu.be/0ZjovHU6ZpY
image: cover.png
---
By the end of this page you will know what dunder methods are and why `print(obj)` calls one, how `@property` makes a method read like an attribute, when to use `@classmethod`, and what `super()` does in a subclass. It builds on [Python decorators](/articles/python/intermediate/decorators/) and the [classes intro](/articles/python/beginner/classes-intro/).

## Python classes and dunder methods

Python runs your classes through special methods whose names start and end with double underscores, called dunder methods. Print an object and Python calls `__repr__`. Add two objects and it calls `__add__`. Compare them and it calls `__eq__`. You never call them yourself: you define them, and the syntax calls them for you.

Here is the whole example. It is used for every section below.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"

    @property
    def shout(self):
        return self.name.upper() + "!"

    @classmethod
    def unnamed(cls):
        return cls("Nobody")

class Dog(Animal):
    def __init__(self, name, tricks=0):
        super().__init__(name)
        self.tricks = tricks

print(Dog("Rex", 3))
print(Dog("Rex").shout)
print(Dog.unnamed())
```

```output
Dog('Rex')
REX!
Dog('Nobody')
```

`__init__` sets up a new object. `__repr__` decides what `print` shows: the class name and the name, so `Dog('Rex')`.

## property: a method that reads like an attribute

Put `@property` above a method and callers write `rex.shout` with no brackets. The value is computed each time it is read, so it can never go stale. Later you can add checks inside it without changing a single caller. A property with no setter is read-only: `rex.shout = "hi"` raises an `AttributeError`.

## Class methods and static methods

There are three kinds of method. A normal method gets `self`, the instance. A class method gets `cls`, the class itself, and is marked with `@classmethod`. A static method, marked with `@staticmethod`, gets neither: it is a plain function that lives inside the class.

Use a class method for alternative constructors. In the example `unnamed` returns `cls("Nobody")`, so `Dog.unnamed()` builds a `Dog`, not an `Animal`, because `cls` is `Dog`.

## Inheritance and super

A subclass inherits everything from its parent. `Dog(Animal)` gets `__repr__`, `shout` and `unnamed` for free. When the child needs its own `__init__`, call `super().__init__(name)` to run the parent's setup first, then add the new attributes. `super()` means the next class up in the chain.

## The Animal and Dog example, line by line

Line 1 defines `Animal`. Lines 2 and 3 store the name. Lines 5 and 6 define `__repr__`. Lines 8 to 10 make `shout` a property. Lines 12 to 14 make `unnamed` a class method. Line 16 declares `Dog` as a subclass of `Animal`. Lines 17 to 19 call `super()` to set the name, then add `tricks`. Line 21 prints a dog, which calls `__repr__`.

## What you learned

- Dunder methods let your objects work with `print`, `+` and `==`.
- `@property` makes a method read like an attribute.
- A class method receives the class, which suits alternative constructors.
- `super()` calls the parent so a subclass can extend instead of replace.

## Common questions

**Do I have to call dunder methods myself?** No. You define `__repr__` and Python calls it when you print the object. Calling `obj.__repr__()` directly works but is almost never what you want.

**What happens if I forget `super().__init__()` in a subclass?** The parent's setup never runs. A `Dog` that defines its own `__init__` without it has no `name`, and reading it raises `AttributeError: 'Dog' object has no attribute 'name'`.

**When should I use `@staticmethod`?** When a function belongs with the class by topic but needs neither the instance nor the class. If you find yourself never using it from the class, a plain module-level function is often clearer.

**Can a property be assigned to?** Not unless you add a setter. Without one, `p.double = 5` raises `AttributeError: property 'double' of 'P' object has no setter`.

**How do I make two objects compare equal?** Define `__eq__`. Without it, `==` on two separate instances compares identity and gives `False`, even when their attributes match. The `@dataclass` shortcut writes `__eq__` for you.

Next in the series: type hints, and how to tell Python and your editor what your code expects.
