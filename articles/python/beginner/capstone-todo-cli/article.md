title: Python to-do list project for beginners: lists, dicts and JSON
summary: Build a small Python to-do app from what you already know: tasks as a list of dictionaries, saved to a JSON file, loaded back with try and except, and printed with enumerate.
description: A Python to-do list project for beginners: a list of dictionaries saved to a JSON file, loaded with try and except, and printed with enumerate. 20 lines.
date: 2026-10-14
read: 4 min read
lesson: 14
video: Build a to-do app | https://youtu.be/__-vu184Egg
image: cover.png
---
By the end of this page you will have a working Python to-do list that remembers its tasks between runs. It uses only things from the earlier lessons: lists, dictionaries, a function, a file, JSON and `try`/`except`.

## The data: a list of dictionaries

Start with the data, because the program is just a way of changing it. One task is a dictionary with two keys: `title`, and `done`, which is `True` or `False`. The whole to-do list is a list of those dictionaries.

Adding a task is `todos.append(...)`. Ticking one off means picking it by position and setting its `done` key: `todos[0]["done"] = True`. Nothing here is new. It is lists and dictionaries working together.

## Save the list to a file

A list in memory disappears when the program ends, so save it. `json.dumps(todos)` turns the list into text, and `path.write_text(...)` puts that text in a file. `json.loads(path.read_text())` does the reverse and gives you the list back.

JSON is a text format that Python lists, dictionaries, strings, numbers, `True`, `False` and `None` map onto. In the file, `True` is written as `true` and `False` as `false`.

## Load it back, even on the first run

The first time the program runs, `todos.json` does not exist, and `path.read_text()` raises `FileNotFoundError`. Wrapping the load in a function with `try` and `except` fixes that: if the file is missing, return an empty list instead.

```python
def load():
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return []
```

The app now starts fresh when there is no file, and remembers everything after that. Catch `FileNotFoundError` by name, not a bare `except`, so a real bug is not hidden.

## The whole program

```python
import json
from pathlib import Path
path = Path("todos.json")


def load():
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return []


todos = load()
todos.append({"title": "Buy milk", "done": False})
todos.append({"title": "Learn Python", "done": False})
todos[0]["done"] = True
path.write_text(json.dumps(todos))
for number, todo in enumerate(todos, start=1):
    mark = "x" if todo["done"] else " "
    print(f"{number}. [{mark}] {todo['title']}")
```

Lines 1 and 2 import `json` and `Path`. Line 3 points at `todos.json`. Lines 6 to 8 define `load`, which tries to read and parse the file, and lines 9 and 10 catch `FileNotFoundError` and return an empty list. Line 13 calls `load`. Lines 14 and 15 append two tasks, and line 16 marks the first one done. Line 17 saves everything to the file. Line 18 loops over the tasks with `enumerate`, starting the count at one. Line 19 picks an `x` or a space, and line 20 prints each task.

Running it prints:

```output
1. [x] Buy milk
2. [ ] Learn Python
```

The file on disk holds the same list, ready for the next run.

## What you learned

- A task is a dictionary, and a to-do list is a list of those dictionaries.
- `json.dumps` and `write_text` save a list, and `read_text` and `json.loads` bring it back.
- `try` and `except FileNotFoundError` let a program start when its file does not exist yet.
- `enumerate(todos, start=1)` gives each item a number for printing.

## Common questions

**Why `json.dumps` and `write_text` instead of `json.dump`?** Both work. `dumps` returns a string, so it pairs with `Path.write_text` and keeps the program short. `json.dump` writes straight to an open file.

**Why does the file show `true` instead of `True`?** JSON has its own spelling. Python's `True`, `False` and `None` are written `true`, `false` and `null`, and `json.loads` converts them back.

**What happens if `todos.json` is empty?** `json.loads("")` raises `json.JSONDecodeError`, which is a different error from `FileNotFoundError`, so this `load` would not catch it. Delete the file or write `[]` into it.

**Why do the tasks double every time I run it?** Each run loads the saved list and then appends the two tasks again. A real app would read each task from the user, for example with `input()`, instead of writing them into the program.

**Where do I go from here?** Add a delete command, a due date key on each task, or a function for each action. Those are the same lists, dictionaries and functions, used a little more.

That finishes the Python beginner track. Next in the series: the Intermediate track begins with Big O in Python, and how to measure what your code costs.
