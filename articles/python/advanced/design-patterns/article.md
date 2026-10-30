title: Python design patterns: strategy, observer, factory and singleton
summary: How the classic design patterns look in Python: strategy as a function you pass in, observer as a list of functions, factory as a dict from a name to a function, and singleton as a module or functools.cache. Three short programs with their real output, and when the class version is still worth writing.
description: Python design patterns with plain functions: strategy, observer, factory and singleton, using a dict, a list and functools.cache, with real code and real output.
date: 2026-10-29
read: 8 min read
lesson: 11
video: Python design patterns | https://youtu.be/PLUZ30XC2Ug
image: cover.png
---
By the end of this page you will know four design patterns the Pythonic way: strategy, observer, factory and singleton. A design pattern is a name for a shape of code that people keep writing. In Java or C#, the books show each one as a pile of classes and interfaces. In Python most of that pile disappears, because functions are objects: you can store them in a variable, pass them to another function, and keep them in a list or a dict. You will see what each pattern is for, how little code it needs, and when the heavier class version is still worth it. It follows [Python profiling and performance](/articles/python/advanced/profiling-and-performance/).

## Strategy: pass a function in

The problem: one piece of code has to do a step in different ways, and you want to pick the way at run time. Think of a shop that prices an order as standard, on sale, or with a student discount. The classic answer is a base class with one subclass per rule. In Python, a strategy is just a function. Write one function per rule, all taking a price and returning a price. The code that needs a rule takes a function as an argument and calls it. Changing the behaviour means passing a different function, and a `lambda` works for a rule you only need once. The only agreement is the signature: every rule takes a price and gives one back.

## Factory: a dict from a name to a function

The problem: you want to create or choose something by a name, often a string from a config file or a user, and you do not want `if` and `elif` branches scattered through the code. In Python the factory is a dictionary that maps a name to a function or a class. Adding a new kind means adding one entry, and the code that uses the factory does not change. Handle the name that is not there: a raw lookup raises a `KeyError`, which says little, so check first and raise a `ValueError` that names the bad value.

Here are both patterns in one program:

```python
def standard(price):
    return price

def sale(price):
    return round(price * 0.8, 2)

def student(price):
    return max(price - 5, 0)

RULES = {"standard": standard, "sale": sale, "student": student}

def make_rule(name):
    if name not in RULES:
        raise ValueError(f"unknown rule: {name}")
    return RULES[name]

def checkout(price, rule):
    return rule(price)

print(checkout(40, standard))
print(checkout(40, make_rule("sale")))
print(checkout(3, make_rule("student")))
print(checkout(40, lambda p: p - 10))
```

Output:

```
40
32.0
0
30
```

`standard` leaves 40 as it is. `sale` takes twenty percent off and rounds to cents. `student` takes five off but never goes below zero, so a price of 3 gives `0` and not minus two. `RULES` is the factory registry, `make_rule` is the factory, and `checkout` is the heart of strategy: it takes a price and a rule and calls the rule, knowing nothing about discounts. Asking `make_rule` for `"holiday"` raises `ValueError: unknown rule: holiday`.

## Observer: a list of functions

The problem: when something happens, several other parts of the program need to know, and the thing that happened should not know who they are. A button is clicked, one part logs it, another counts it. The classic version defines an observer interface and a subject that keeps a list of observers. In Python an observer is a function, and the subject keeps a plain list of them. `subscribe` appends one. When the event happens, the subject loops over the list and calls each function with the event.

Two details matter. To unsubscribe, remove the function, but check it is in the list first so removing twice does not crash. And loop over a copy of the list, `list(self.listeners)`, so a listener that unsubscribes itself while it runs does not make the loop skip the next one.

```python
class Button:
    def __init__(self):
        self.listeners = []

    def subscribe(self, fn):
        self.listeners.append(fn)

    def unsubscribe(self, fn):
        if fn in self.listeners:
            self.listeners.remove(fn)

    def click(self):
        for fn in list(self.listeners):
            fn("clicked")

def log(event):
    print("log:", event)

button = Button()
button.subscribe(log)
button.subscribe(lambda e: print("count:", e))
button.click()
button.unsubscribe(log)
button.unsubscribe(log)
button.click()
```

Output:

```
log: clicked
count: clicked
count: clicked
```

The first click reaches both listeners. Then `log` is removed, and removing it a second time does nothing and does not crash. The second click reaches only the `count` listener. The button never needs to know what its listeners do, and listeners can come and go while the program runs.

## Singleton: a module or functools.cache

The problem: you want exactly one shared object, such as the settings of a program, and every part of the code should get that same object. The classic answer is a class that overrides how instances are created and blocks a second one. Python gives you two simpler ways.

The first is that a module is already a singleton. Python imports a module once and keeps it, so a variable at the top of a module is the same object everywhere it is imported. The second is a function wrapped in `functools.cache`:

```python
from functools import cache

@cache
def get_config():
    print("loading")
    return {"debug": True}

a = get_config()
b = get_config()
print(a is b)
```

Output:

```
loading
True
```

`loading` prints once, on the first call. The second call does not run the body at all: `cache` hands back the stored dictionary, so `a is b` is `True`. One object, created once, shared by everyone who asks.

Be careful though. A singleton is shared global state: any code can change it, and tests that run one after another can leak changes into each other. Use one when sharing is the point, and otherwise pass the object in as an argument.

## What you learned

- In Python, a pattern is often just a function.
- Strategy: pass a function to the code that needs the choice.
- Observer: keep a list of functions, loop over a copy, and check before you remove.
- Factory: a dict from a name to a function or class, with a clear `ValueError` for an unknown name.
- Singleton: a module variable, or a function wrapped in `functools.cache`.
- Reach for the full class version only when the pieces need their own state or several methods that belong together.

## Common questions

**What is the strategy pattern in Python?** A way to choose how a step is done at run time. In Python the strategies are plain functions with the same signature, and the code that needs one takes a function as an argument and calls it.

**Why loop over a copy of the listeners in the observer pattern?** If a listener removes itself from the list while the loop is running, the list shrinks under the loop and the next listener is skipped. Looping over `list(self.listeners)` avoids that.

**Why raise `ValueError` instead of letting the dict raise `KeyError`?** A `KeyError` shows only the missing key. A `ValueError` with a message such as `unknown rule: holiday` tells the reader what went wrong and where to look.

**Is `functools.cache` a real singleton?** It gives the behaviour you want from one: the function body runs once and every later call returns the same object. It is not a class that blocks a second instance, which is rarely needed in Python.

**Are singletons a good idea?** Only when sharing really is the point. They are global state, so code that uses one is harder to test. Passing the object in as an argument is usually easier to change.

**When is the class version still worth it?** When the pieces need their own state or several methods that belong together, such as a strategy that keeps a running total, or an observer that must carry its own settings.

Next in the series is [context managers and protocols](/articles/python/advanced/context-managers-and-protocols/).
