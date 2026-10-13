title: Python classes for beginners: __init__, self, methods and @dataclass
summary: Build your own type with class, store data on it with __init__ and self, give it behaviour with methods, print it clearly with __repr__, and see the @dataclass shortcut.
description: Python classes for beginners: class, instances, __init__, self, attributes, methods, __repr__ and the @dataclass shortcut, with code you can run.
date: 2026-10-13
read: 4 min read
lesson: 13
video: Classes | https://youtu.be/dTO4D7Yz-_Y
image: cover.png
---
So far you have used types that Python gave you: `int`, `str`, `list`, `dict`. By the end of this page you will build your own type with `class`, give it data and behaviour, and know the shortcut Python offers for simple classes.

## What a class is

A class is a blueprint for your own type. `class Dog:` creates a new kind of thing. Calling `Dog("Rex", 3)` builds one real dog from the blueprint, and that dog is called an instance. You can build as many instances as you like, and each one keeps its own data.

## __init__, self and attributes

When you call `Dog("Rex", 3)`, Python builds an empty object and then runs a special method named `__init__` to set it up. Its first parameter is `self`, the new object. Inside it, `self.name = name` stores the name on that object. Values stored on an object this way are its attributes.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Because every instance has its own `self`, two dogs from the same class do not share their names or ages.

## Methods

A method is a function that lives inside a class. It always takes `self` first, so it knows which object it was called on. When you write `rex.bark()`, Python passes `rex` in as `self`.

```python
    def bark(self):
        return f"{self.name} says woof"
```

## __repr__

By default, printing an object shows something unhelpful, such as `<__main__.Dog object at 0x...>`, which is a memory address. Add a `__repr__` method to decide how the object prints. Inside the f-string, `{self.name!r}` formats the name with `repr()`, so a string keeps its quotes and the result looks like the code that would build the object.

```python
    def __repr__(self):
        return f"Dog({self.name!r}, {self.age})"
```

## The @dataclass shortcut

Writing `__init__` and `__repr__` by hand gets repetitive. For classes that mostly hold data, Python has a decorator in the standard library. List the fields with their types, and Python writes `__init__` and `__repr__` for you.

```python
from dataclasses import dataclass


@dataclass
class Dog:
    name: str
    age: int
```

`Dog("Rex", 3)` now prints as `Dog(name='Rex', age=3)`. That is four lines instead of seven for the same object.

## The whole program, line by line

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} says woof"

    def __repr__(self):
        return f"Dog({self.name!r}, {self.age})"


rex = Dog("Rex", 3)
print(rex.bark())
print(rex.age)
print(rex)
```

```output
Rex says woof
3
Dog('Rex', 3)
```

Line 1 defines the `Dog` class. Line 2 is `__init__`, taking a name and an age. Lines 3 and 4 store them on `self`. Line 6 is the `bark` method, and line 7 builds a string from the name. Line 9 is `__repr__`, and line 10 returns how a dog should print. Line 13 creates a dog called Rex, aged 3. Line 14 calls `bark`. Line 15 prints the `age` attribute. Line 16 prints the dog itself, using `__repr__`.

## What you learned

- A class is a blueprint, and calling it builds an instance.
- `__init__` sets up each new object, and `self` is the object itself.
- Values stored with `self.name = name` are attributes.
- A method is a function inside a class that takes `self` first.
- `__repr__` decides how an object prints, and `@dataclass` writes `__init__` and `__repr__` for you.

## Common questions

**What is the difference between a class and an instance?** The class is the blueprint, `Dog`. An instance is one object built from it, such as `rex = Dog("Rex", 3)`. One class can have many instances.

**Why does every method take self?** Python passes the object you called the method on as the first argument. In `rex.bark()`, `self` is `rex`, which is how the method finds `self.name`.

**What happens if I forget an argument?** `__init__` is called with whatever you pass, so a missing one is an error. `Dog()` raises `TypeError: Dog.__init__() missing 2 required positional arguments: 'name' and 'age'`.

**What does `!r` do in an f-string?** It formats the value with `repr()` instead of `str()`. For a string, that keeps the quotes: `'Rex'` instead of `Rex`.

**When should I use @dataclass?** When a class mostly holds values. It writes `__init__` and `__repr__` for you, and two dataclass instances with the same values compare as equal with `==`.

This lesson follows on from [Python modules, import and uv](/articles/python/beginner/modules-and-uv/). Next in the series: the beginner capstone, a to-do list command line app.
