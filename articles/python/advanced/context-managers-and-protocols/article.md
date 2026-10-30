title: Python context managers and protocols: with, contextlib, Protocol
summary: What the with statement really calls, how to write your own context manager as a class or with @contextmanager, what contextlib gives you for free, and how typing.Protocol matches a class by its methods instead of its parents. Three short programs with their real output.
description: Python context managers and protocols: how with calls __enter__ and __exit__, @contextmanager, contextlib.suppress, and typing.Protocol, with real code and output.
date: 2026-10-30
read: 7 min read
lesson: 12
video: Python context managers and protocols | https://youtu.be/XARnqMbPbI8
image: cover.png
---
By the end of this page you will know exactly what a Python `with` statement does behind the scenes, how to write your own context manager in two ways, which tools `contextlib` gives you for free, and how a `Protocol` lets you describe what an object can do instead of what it inherits from. You already use both ideas: every `with` block is a context manager, and every `for` loop relies on a protocol. It follows [Python design patterns](/articles/python/advanced/design-patterns/).

## The problem: cleanup that must happen

Some things must be undone: a file must be closed, a lock released, a temporary change put back. The manual way is `try` and `finally`: open the resource, try the work, and clean up in `finally`. It works, but every place that uses the resource repeats that shape, and one forgotten `finally` leaks the resource. A context manager moves the cleanup into the object itself, so the caller just writes `with`, and the cleanup is guaranteed.

## What with really calls

`with` is a protocol: a small agreement with two methods. When the block starts, Python calls `__enter__` on the object, and whatever it returns is bound to the name after `as`. Then the block runs. When the block ends, however it ends, Python calls `__exit__`. A normal finish, an exception, a `return` or a `break`: `__exit__` always runs. That is the whole guarantee.

## What __exit__ receives and returns

`__exit__` takes three arguments: the exception type, the exception value and the traceback. If the block finished normally, all three are `None`. If the block raised, they describe the error. Then `__exit__` decides what happens to that error. If it returns a true value, the exception is suppressed and the program carries on after the `with` block. If it returns false or `None`, which is the default, the exception goes on up as normal. Be careful: swallowing errors by accident hides bugs, so suppress only the exact type you mean to.

Here is a class based context manager that does all of this:

```python
class Section:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("enter", self.name)
        return self

    def __exit__(self, exc_type, exc, tb):
        print("exit", self.name, exc_type)
        return exc_type is KeyError

with Section("a") as s:
    print("inside", s.name)

with Section("b"):
    {}["x"]
print("after b")

try:
    with Section("c"):
        int("x")
except ValueError:
    print("caught")
```

Output:

```
enter a
inside a
exit a None
enter b
exit b <class 'KeyError'>
after b
enter c
exit c <class 'ValueError'>
caught
```

`__enter__` prints and returns `self`, so `as s` can use it. `__exit__` prints the exception type and returns `True` only when that type is `KeyError`. Section `a` finishes normally, so `__exit__` sees `None`. Section `b` looks up a missing key, which raises a `KeyError`; `__exit__` returns `True`, the error is swallowed, and `after b` still prints. Section `c` raises a `ValueError`, `__exit__` returns `False`, and the error goes on up to the `except`, which prints `caught`. `__exit__` ran in all three cases. Only what it did with the error differed.

## contextlib: @contextmanager and suppress

A class for every context manager is a lot of ceremony. The `contextlib` module shortens it. The `@contextmanager` decorator turns a generator function into a context manager. Everything before the `yield` is the enter part, the yielded value is what `as` receives, and everything after the `yield` is the exit part. Put the `yield` inside `try` and `finally`, so the cleanup runs even when the block raises.

`contextlib` also has ready made tools. `suppress` ignores the exception types you list, `closing` calls `close()` for you, `redirect_stdout` captures printing, and `ExitStack` lets you enter a number of context managers that you only know about at run time.

```python
from contextlib import contextmanager, suppress

@contextmanager
def tag(name):
    print("open", name)
    try:
        yield name
    finally:
        print("close", name)

with tag("p") as t:
    print("hello", t)

with suppress(FileNotFoundError):
    open("missing.txt")
print("still running")
```

Output:

```
open p
hello p
close p
still running
```

`open p`, `hello p`, `close p`: the cleanup ran after the block. The missing file raised nothing, because `suppress(FileNotFoundError)` swallowed exactly that one error type, and `still running` is printed. It is the same behaviour as the class, in a handful of lines.

## Protocols and duck typing

You have just seen one protocol, the `with` protocol, which is nothing more than two methods. Python is full of them. If an object has `__iter__`, a `for` loop accepts it. If it has `__len__`, `len()` works on it. Nobody had to inherit from a special base class. This is duck typing: if it walks like a duck and quacks like a duck, it is a duck. The weakness is that nothing writes the agreement down, so a type checker cannot help you.

## typing.Protocol: structural typing

The `typing` module fixes that with `Protocol`. You write a class that inherits from `Protocol` and list the methods an object must have. That is a structural type: any class with those methods matches, whether or not it mentions the `Protocol` anywhere. The checker compares shapes, not family trees. A normal base class is nominal typing: you only count if you inherit by name.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Speaker(Protocol):
    def speak(self) -> str: ...

class Dog:
    def speak(self) -> str:
        return "woof"

class Robot:
    def speak(self) -> str:
        return "beep"

def talk(x: Speaker) -> None:
    print(x.speak())

talk(Dog())
talk(Robot())
print(isinstance(Dog(), Speaker))
print(isinstance(5, Speaker))
```

Output:

```
woof
beep
True
False
```

`Speaker` describes one method, `speak`, and the three dots are its body because a `Protocol` only describes. `Dog` and `Robot` each have a `speak` method and neither mentions `Speaker`, yet `talk` accepts both. A type checker would accept both calls and reject a class with no `speak`. With `@runtime_checkable`, `isinstance` works too: `True` for the dog, `False` for the number 5. Know its limit: at run time it only checks that the method names exist, not their signatures or what they return.

## What you learned

- `with` calls `__enter__` at the start and `__exit__` at the end, always.
- `__exit__` receives the exception type, value and traceback; returning true swallows the error.
- `@contextmanager` writes a context manager as a generator, with the `yield` inside `try` and `finally`.
- Reach for `suppress`, `closing` and `ExitStack` before writing your own.
- A protocol is an agreement on methods. `typing.Protocol` makes it checkable: any class with the right methods matches, with no inheritance.

## Common questions

**What is a context manager in Python?** An object with `__enter__` and `__exit__` methods that you use in a `with` statement. Python calls `__enter__` when the block starts and `__exit__` when it ends, so cleanup always happens.

**Does __exit__ run if the block raises an exception?** Yes. It runs on a normal finish, on an exception, and on `return` or `break`. It receives the exception details, and if it returns true the exception is swallowed.

**Why put the yield inside try and finally in @contextmanager?** If the block raises, the exception is thrown into the generator at the `yield`. Without `try` and `finally`, the code after the `yield` would be skipped and the cleanup would not run.

**What is the difference between a Protocol and a base class?** A base class is nominal: a class matches only if it inherits from it by name. A `Protocol` is structural: any class with the right methods matches, even if it has never heard of the `Protocol`.

**Does isinstance check the full shape of a Protocol?** No. With `@runtime_checkable` it only checks that the method names exist. Signatures and return types are the job of a type checker.

Next in the series is template strings.
