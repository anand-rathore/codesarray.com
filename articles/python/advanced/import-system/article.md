title: Python import system explained: sys.modules, sys.path, importlib and circular imports
summary: How the Python import system works: modules and packages, why a module runs only once, how sys.path decides where Python looks, relative imports, importlib, circular imports and how to fix them, and lazy import coming in Python 3.15. Four short programs with their real output.
description: Python import system explained: sys.modules, sys.path, relative imports, importlib, circular imports and lazy import, with runnable code and real output.
date: 2026-10-28
read: 8 min read
lesson: 9
video: Python import system explained | https://youtu.be/AMXGAESE21U
image: cover.png
---
By the end of this page you will know what the Python import system really does when it sees `import`: how a module differs from a package, why a module runs only once, where Python looks and in what order, why relative imports fail in a script, how to import by name with `importlib`, and why circular imports break and how to fix them. It follows [descriptors and metaclasses](/articles/python/advanced/descriptors-and-metaclasses/).

## Modules and packages

A **module** is one `.py` file. A **package** is a folder of modules, normally with a file called `__init__.py`, which is the package's own module and runs when you import the package. The examples use a package called `shop` with three files:

```python
# shop/__init__.py
print("loading shop")
from .prices import total
```

```python
# shop/prices.py
print("loading prices")
from . import tax


def total(amount):
    return round(amount * (1 + tax.RATE), 2)
```

```python
# shop/tax.py
print("loading tax")
RATE = 0.2
```

`import shop.tax` imports `shop` first, then `tax` inside it, but binds only the name `shop` in your code; you reach the module as `shop.tax`. A folder without `__init__.py` still works as a namespace package, but when you write your own package, add the file.

## What import does: sys.modules

Four steps. Python looks in `sys.modules`, a dictionary of every module already loaded; if the name is there, you get that same module back and nothing runs. If not, it finds the file, creates a module object and registers it in `sys.modules`, runs the file's code inside it, and binds the name in your code. So a module runs once per program, and a second import is only a dictionary lookup.

```python
import sys
import shop
import shop

print(shop.total(10))
print(shop.prices.__package__)
print(sorted(m for m in sys.modules if m.startswith("shop")))
```

```output
loading shop
loading prices
loading tax
12.0
shop
['shop', 'shop.prices', 'shop.tax']
```

`shop` started first but finished last, because it needed `prices`, and `prices` needed `tax`. The second `import shop` printed nothing. Because a module is a shared object, a change one file makes to it is seen by every other file.

## Where Python looks: sys.path

When the module is not in `sys.modules`, Python walks the list `sys.path` in order and takes the first match. Index zero is the folder of the script you ran, then the folders in the `PYTHONPATH` environment variable, then the standard library, then `site-packages`, where `pip` and `uv` install dependencies.

That order explains a classic bug: name your own file `random.py` or `json.py` and `import random` finds your file, because your folder comes first. If a standard module acts strangely, print its `__file__`.

## Relative imports

Inside a package you can name a sibling two ways. An absolute import gives the full path from the top: `from shop.tax import RATE`. A relative import counts from the current package: one dot is this package, two dots are the parent. `prices.py` says `from . import tax`, meaning from my own package, import `tax`.

Relative imports work only inside a package. Run a file in the package directly, as in `python shop/prices.py`, and its name is `__main__` with no package, so Python raises `ImportError: attempted relative import with no known parent package`. Run it as a module instead, `python -m shop.prices`, or put the entry point outside the package.

## importlib: import by name

The `import` statement needs the name written in the source. When the name is only known at run time, such as a plugin or a setting, use `importlib`:

```python
import importlib
import importlib.util
import sys
from pathlib import Path

print(Path(sys.path[0]) == Path(__file__).parent)
print(importlib.util.find_spec("nothing_here"))
tax = importlib.import_module("shop.tax")
print(tax.RATE)
tax.RATE = 0.5
print(importlib.import_module("shop.tax").RATE)
importlib.reload(tax)
print(tax.RATE)
```

```output
True
None
loading shop
loading prices
loading tax
0.2
0.5
loading tax
0.2
```

The script's folder is first on `sys.path`. `find_spec` returns `None` for a module that does not exist, which makes it a safe way to ask whether something is installed. `import_module` goes through the same cache, so after the rate is changed to `0.5`, importing again shows `0.5`. `reload` runs the file again inside the same module object, so the rate is back to `0.2`. Names imported with `from ... import` still point at the old objects after a reload, so use it for experiments, not production.

## Circular imports

File `cyc_a` imports `cyc_b`, and `cyc_b` asks for a name from `cyc_a`:

```python
# cyc_a.py
print("cyc_a starts")
import cyc_b


def hello():
    return "hi from a"
```

```python
# cyc_b.py
print("cyc_b starts")
from cyc_a import hello

print("cyc_b ends")
```

Python starts `cyc_a` and puts it into `sys.modules` half built. Line two imports `cyc_b`, which asks for `hello` from `cyc_a`, but `cyc_a` has not reached its `def` yet. The name is missing, so you get `ImportError`. Compare the fixed pair, where `good_b` imports the module and uses it only inside a function:

```python
# good_a.py
print("good_a starts")
import good_b


def hello():
    return "hi from a"
```

```python
# good_b.py
print("good_b starts")
import good_a


def shout():
    return good_a.hello().upper()
```

```python
try:
    import cyc_a
except ImportError as err:
    print(type(err).__name__, "-", str(err).split(" (")[0])

import good_a
print(good_a.good_b.shout())
```

```output
cyc_a starts
cyc_b starts
ImportError - cannot import name 'hello' from 'cyc_a'
good_a starts
good_b starts
HI FROM A
```

There are three fixes. Best: move the shared code to a third module that both files import, so the cycle disappears. Second: import the module, not the name, and use it later, as `good_b` does. Third, a last resort: import inside the function that needs it.

## Lazy import

Imports cost time, and a big library imported at the top of a command line tool slows start-up even when the user only asked for help. Python 3.15, which is coming, adds a soft keyword for this: `lazy import json` binds the name to a placeholder and loads the real module on first use, and `lazy from json import dumps` does the same for a name. It is allowed only at the top level of a file, not in functions or `try` blocks, and not with star imports. You cannot run it on 3.14, but `importlib.util.LazyLoader` gives the same behaviour today:

```python
import importlib.util
import sys


def lazy(name):
    spec = importlib.util.find_spec(name)
    spec.loader = importlib.util.LazyLoader(spec.loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


slow = lazy("slow")
print("imported")
print(slow.VALUE)
```

```output
imported
loading slow
42
```

`imported` prints first and the file has not run. On the first attribute access, `loading slow` appears and then the value.

## What you learned

- A module is a file; a package is a folder, usually with `__init__.py`.
- Import checks `sys.modules` first, so a module runs once and is shared.
- Otherwise Python walks `sys.path` and the first match wins, with your own folder first.
- Relative imports count from the current package and fail in a script run directly.
- `importlib` imports by name, finds specs and reloads.
- A circular import fails because the other file is half loaded; move shared code out, or import the module and use it later.
- `lazy import`, coming in Python 3.15, delays loading until first use.

## Common questions

**Why does my import run the file only once?** Because the module is stored in `sys.modules` after the first import, and later imports return that stored object.

**Why does import find my file instead of the standard library?** `sys.path` starts with your script's folder, so a file called `random.py` there wins. Rename it.

**What does attempted relative import with no known parent package mean?** You ran a file inside a package as a script, so it has no package for the dots to count from. Run it with `python -m shop.prices`.

**How do I fix a circular import?** Move the shared code to a third module, or import the module instead of the name and use it inside a function.

**Is lazy import available now?** Not yet: it is coming in Python 3.15. On 3.14, use `importlib.util.LazyLoader` as shown above.

Next in the series is profiling and performance.
