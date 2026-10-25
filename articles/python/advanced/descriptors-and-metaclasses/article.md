title: Python descriptors and metaclasses explained: property, __set_name__ and __init_subclass__
summary: How Python descriptors work: __get__ and __set__ on the class, how property is built from one, a reusable Positive descriptor with __set_name__, data versus non data descriptors, __init_subclass__ for a plugin registry, and when a metaclass is the right tool. Five short programs with their real output.
description: Python descriptors and metaclasses explained: __get__, __set__, property, __set_name__, __init_subclass__ and metaclasses, with runnable code and real output.
date: 2026-10-25
read: 7 min read
lesson: 8
video: Python descriptors and metaclasses explained | https://youtu.be/QjVUz2wXxqI
image: cover.png
---
By the end of this page you will know how Python descriptors work: why `item.price` can run your own code, how `property` is built from one, how a single descriptor can guard many fields, and how `__init_subclass__` and metaclasses hook into class creation. It follows [memory management and the garbage collector](/articles/python/advanced/memory-model-and-gc/).

## How Python looks up an attribute

When you write `item.price`, Python does not simply look in a dictionary. It looks at the class first. If the class holds an object for that name and the object has a `__get__` method, Python calls it, and what it returns is the value. An object like that is a **descriptor**.

The protocol has three methods: `__get__` runs on a read, `__set__` runs on an assignment, and `__delete__` runs on `del`. A descriptor lives on the class but is called with the instance, so one object serves every instance.

## property is a descriptor

You have already used one. Reading `t.f` calls the getter, and with `@f.setter` assigning to it calls the setter.

```python
class Temp:
    def __init__(self, celsius):
        self._c = celsius

    @property
    def f(self):
        return self._c * 9 / 5 + 32

    @f.setter
    def f(self, value):
        self._c = (value - 32) * 5 / 9


t = Temp(100)
print(t.f)
t.f = 32
print(t._c)
print(type(Temp.f).__name__)
print(Temp.f.fget.__name__)
```

```output
212.0
0.0
property
f
```

A hundred Celsius is 212 Fahrenheit. Assigning 32 runs the setter, so the stored Celsius becomes 0. Nothing is stored under `f` on the instance: `Temp.f` is a `property` object on the class, and its getter is kept as `fget`.

## A reusable descriptor with __set_name__

A property suits one attribute. If many attributes need the same rule, write the rule once as a descriptor class. The descriptor is shared, so it must know which attribute it serves. Python tells it: when the class body finishes, it calls `__set_name__(owner, name)` on every descriptor in the class.

```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.name[1:]} must be positive")
        setattr(obj, self.name, value)


class Item:
    price = Positive()
    qty = Positive()

    def __init__(self, price, qty):
        self.price = price
        self.qty = qty


item = Item(9.5, 3)
print(item.price * item.qty)
print(type(Item.price).__name__)
try:
    item.price = -1
except ValueError as error:
    print(error)
print(item.price)
```

```output
28.5
Positive
price must be positive
9.5
```

`price` and `qty` both use `Positive`. The value is stored on the instance under a private name (`_price`, `_qty`). When you ask the class itself, `Item.price`, the instance is `None`, so `__get__` returns the descriptor, and the second line prints its type. The rejected `-1` never reaches the object, so the old `9.5` is kept.

## The mistake: storing the value on the descriptor

Do not write `self.value = value` inside a descriptor. There is only one descriptor per class, so every instance would share that one value: set the price of one item and every item changes. Keep the value on the instance, under a private name or in its `__dict__`. If you must keep data on the descriptor, key it by instance with a `weakref.WeakKeyDictionary`.

## Data and non data descriptors

Which wins when the class and the instance both have the name? A **data descriptor** defines `__set__` or `__delete__` as well as `__get__`, and it beats the instance `__dict__`. A **non data descriptor** has only `__get__`, and the instance `__dict__` beats it.

```python
class Loud:
    def __get__(self, obj, owner=None):
        return "descriptor"

    def __set__(self, obj, value):
        pass


class Quiet:
    def __get__(self, obj, owner=None):
        return "descriptor"


class Box:
    loud = Loud()
    quiet = Quiet()

    def hi(self):
        return "hi"


b = Box()
b.__dict__["loud"] = "instance"
b.__dict__["quiet"] = "instance"
print(b.loud)
print(b.quiet)
print(type(Box.hi).__name__, type(b.hi).__name__)
print(b.hi.__self__ is b)
```

```output
descriptor
instance
function method
True
```

`loud` is a data descriptor, so the class wins even though the instance dictionary holds an entry. `quiet` has only `__get__`, so the instance value wins. That is also why a property cannot be overwritten through `__dict__`.

Plain functions are non data descriptors. `Box.hi` on the class is a function, but `b.hi` runs the function's `__get__`, which returns a bound method with `b` already filled in as `self`. The last line confirms `b.hi.__self__ is b`.

## __init_subclass__

Descriptors hook into attributes. `__init_subclass__` hooks into class creation: Python calls it on the parent every time a subclass is defined. It is an implicit class method, extra keywords in the class line are passed to it, and it should call `super().__init_subclass__(**kwargs)` so other classes in the chain run their hooks too. It arrived in Python 3.6.

```python
class Plugin:
    registry = {}

    def __init_subclass__(cls, /, key=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.registry[key or cls.__name__.lower()] = cls


class Csv(Plugin):
    pass


class Json(Plugin, key="js"):
    pass


print(sorted(Plugin.registry))
print(Plugin.registry["js"] is Json)
print(Plugin.registry["csv"].__name__)
```

```output
['csv', 'js']
True
Csv
```

Nobody called a register function. `Csv` and `Json` registered themselves when they were defined, and `key="js"` came straight from the class line. A plugin registry in a few lines replaces the most common reason to write a metaclass.

## Classes are objects: type and metaclasses

A class is an instance of `type`, and `type` is an instance of itself. Calling `type(name, bases, namespace)` builds a class, and a `class` statement is a nicer way of writing that call. A **metaclass** is a class whose instances are classes: inherit from `type` and choose it with `metaclass=` in the class line.

```python
Dog = type("Dog", (), {"sound": "woof"})
print(Dog().sound, type(Dog).__name__, type(type).__name__)


class Meta(type):
    def __new__(mcls, name, bases, ns):
        ns["fields"] = [k for k in ns if not k.startswith("_")]
        return super().__new__(mcls, name, bases, ns)

    def __iter__(cls):
        return iter(cls.fields)


class Point(metaclass=Meta):
    x = 0
    y = 0


print(Point.fields)
print(list(Point))
print(type(Point).__name__)
```

```output
woof type type
['x', 'y']
['x', 'y']
Meta
```

`Meta.__new__` runs while `Point` is being created and changes the namespace before the class exists, adding a `fields` list found at that moment. `__iter__` defined on the metaclass makes the class itself loopable, which is how enums let you loop over their members. The type of `Point` is `Meta`, not `type`.

## Which tool to use

Start with the lightest tool:

1. One attribute with custom behaviour: a `property`.
2. The same rule on many attributes: a descriptor with `__set_name__`.
3. React when a subclass is created: `__init_subclass__`.
4. Change the class as it is built, or give the class itself new behaviour: a metaclass, and only then.

A class can have only one metaclass, and two libraries with different metaclasses cannot be combined: Python raises a metaclass conflict. You will meet metaclasses in enums, abstract base classes and object mappers, and rarely need to write one.

## What you learned

- A descriptor is an object on the class with `__get__` and optionally `__set__` and `__delete__`.
- A data descriptor beats the instance `__dict__`; a non data descriptor loses to it.
- `property` and plain functions are descriptors.
- `__set_name__` tells a descriptor its name, and the value belongs on the instance, never on the descriptor.
- `__init_subclass__` runs for every new subclass and handles most registry jobs.
- A metaclass is a class whose instances are classes, and the default one is `type`.

## Common questions

**Is property a descriptor?** Yes. `type(Temp.f)` is `property`, an object on the class with `__get__` and `__set__`, and its getter is stored in `fget`.

**Why can't I store the value on the descriptor?** Because one descriptor serves every instance of the class, so they would all share a single value. Store it on the instance.

**What is the difference between a data and a non data descriptor?** A data descriptor defines `__set__` or `__delete__`, so it wins over the instance `__dict__`. A non data descriptor, such as a plain function, loses to it.

**Do I need a metaclass for a plugin registry?** No. `__init_subclass__` does it in a few lines, as in the example above.

**Why can't I mix two metaclasses?** A class can have only one metaclass, so Python raises a metaclass conflict if two bases disagree. Prefer `__init_subclass__` or a descriptor when they are enough.

Next in the series is the import system.
