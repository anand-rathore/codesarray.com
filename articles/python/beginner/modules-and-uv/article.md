title: Python modules, import and uv: the standard library, packages and pyproject.toml
summary: Use code other people wrote with import, from and as, install packages with uv add, keep each project in its own virtual environment, and tidy it with pyproject.toml and ruff.
description: Python modules, import and uv for beginners: import, from and as, the standard library, uv init, add and run, virtual environments, pyproject.toml and ruff.
date: 2026-10-13
read: 4 min read
lesson: 12
video: Modules and uv | https://youtu.be/O7UeCbjo268
image: cover.png
---
You do not have to write everything yourself. By the end of this page you will import code that other people wrote, set up a project with `uv`, and keep it tidy with a `pyproject.toml` file and `ruff`.

## import and the standard library

A module is just a Python file full of code you can reuse. `import` brings it in. After `import math`, the call `math.sqrt(144)` runs a function that lives inside that module. `from statistics import mean` pulls out one name, so you call `mean` directly. And `as` gives a module a shorter name.

```python
import math
import statistics as stats
from statistics import mean

math.sqrt(144)
stats.mean([88, 92, 79, 95])
```

Python ships with hundreds of modules like these. Together they are called the standard library, and they are already installed.

## uv and pip

Beyond the standard library, other people publish packages. The tool for them is `uv`. Run `uv init` to start a project. Run `uv add requests` to install a package into it. Run `uv run main.py` to run your code with everything it needs.

```
uv init
uv add requests
uv run main.py
```

You will also see `pip install requests` everywhere. It does the same job. `uv` is simply faster, and it manages the environment for you.

## Virtual environments, pyproject.toml and ruff

Each project gets its own virtual environment, a private folder of packages, so one project never breaks another. `uv` creates it for you, in a folder named `.venv`.

The project file is `pyproject.toml`. It lists the project name, its Python version and its dependencies:

```
[project]
name = "demo"
requires-python = ">=3.12"
dependencies = ["requests"]
```

`ruff` keeps the code tidy. Add it to the project, then check and format:

```
uv add --dev ruff
uv run ruff check
uv run ruff format
```

`ruff check` finds mistakes, and `ruff format` tidies your code.

## The whole program

```python
import math
import statistics as stats
from pathlib import Path

scores = [88, 92, 79, 95]

print(math.sqrt(144))
print(math.pi)
print(stats.mean(scores))
print(Path("report.txt").suffix)
```

```output
12.0
3.141592653589793
88.5
.txt
```

Line 1 imports `math`. Line 2 imports `statistics` and calls it `stats`. Line 3 imports `Path` from `pathlib`. Line 5 is a list of scores. Line 7 prints the square root of 144. Line 8 prints pi. Line 9 prints the mean of the scores. Line 10 prints the suffix of a file name. All of it comes from modules we never wrote.

## What you learned

- `import` brings in a module, `as` gives it a shorter name, and `from` pulls out one name.
- The standard library is already installed with Python.
- `uv add` installs a package into your project, and `uv run` runs your code with it.
- `pyproject.toml` describes the project and its dependencies, and `ruff` checks and formats the code.

## Common questions

**What is the difference between a module and a package?** A module is one Python file. A package is a folder of modules, usually something you install, such as `requests`.

**Do I need uv, or is pip enough?** `pip install` works and you will see it in many tutorials. `uv` does the same job faster and also creates and manages the virtual environment for you.

**Why does every project need its own virtual environment?** Two projects can need different versions of the same package. A private `.venv` per project keeps them from breaking each other.

**What does `from statistics import mean` do differently from `import statistics`?** It brings in just the name `mean`, so you write `mean(scores)` instead of `statistics.mean(scores)`.

**What goes in pyproject.toml?** The project name, the Python version it needs, and its dependencies. `uv add` updates the dependencies for you.

This lesson follows on from [Python files and JSON](/articles/python/beginner/files-and-json/). Next in the series: classes.
