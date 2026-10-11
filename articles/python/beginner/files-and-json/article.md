title: Python read and write files and JSON: open, pathlib, json.dump and json.load
summary: Read and write files in Python with open and a with block, build paths with pathlib, and save a dictionary as JSON with json.dump and get it back with json.load.
description: Python read and write files and JSON for beginners: open with a with block, build paths with pathlib, and save data with json.dump and json.load.
date: 2026-10-11
read: 4 min read
lesson: 11
video: Files and JSON | https://youtu.be/jdQt8FiBVeI
image: cover.png
---
Everything your program knows disappears when it ends, unless you save it. By the end of this page you will read and write files safely with `open` and a `with` block, build paths that work on every system with `pathlib`, and save your data as JSON so it outlives your program.

## open and with

To work with a file, call `open` with its name and a mode. `"r"` reads, `"w"` writes and replaces the whole file, and `"a"` adds to the end. Always open inside a `with` block. When the block ends, Python closes the file for you, even if an error happens in the middle.

```python
with open("notes.txt", "w") as f:
    f.write("hi")
```

## pathlib

Build paths with `pathlib`, not by gluing strings together. `Path("data")` makes a path object. The `/` operator joins pieces and uses the right separator on every system. `read_text()` and `write_text()` handle a whole file in one call, and `exists()` tells you whether it is there.

```python
from pathlib import Path

path = Path("data") / "notes.txt"
path.exists()
```

## JSON

JSON is the standard text format for data. `json.dump` turns a dictionary or a list into JSON text in a file. `json.load` reads it back into real Python objects. Strings, numbers, lists and dictionaries all survive the trip, and `True` becomes `true` in the file. For spreadsheet style rows, the `csv` module works the same way.

## The whole program

```python
from pathlib import Path
import json

path = Path("scores.json")
scores = {"ada": 91, "linus": 78}

with path.open("w") as f:
    json.dump(scores, f)

with path.open() as f:
    loaded = json.load(f)

loaded["grace"] = 88
print(loaded)
print(path.read_text())
```

```output
{'ada': 91, 'linus': 78, 'grace': 88}
{"ada": 91, "linus": 78}
```

Line 1 imports `Path`, and line 2 imports `json`. Line 4 makes a path to `scores.json`. Line 5 is a dictionary of scores. Line 7 opens the file for writing inside a `with` block, and line 8 dumps the dictionary into it. Line 10 opens it again, this time to read, and line 11 loads it back into `loaded`. Line 13 adds a new score for grace. Line 14 prints the dictionary, and line 15 prints the raw text of the file. The first output line has grace, because it is in memory. The second has only ada and linus, because we never saved grace.

## What you learned

- `open` takes a mode: `"r"` reads, `"w"` replaces, `"a"` appends, and a `with` block closes the file for you.
- `Path` joins pieces with `/` and reads or writes a whole file with `read_text` and `write_text`.
- `json.dump` saves data to a file, and `json.load` brings it back.
- A change in memory is not in the file until you save it.

## Common questions

**Why use a with block?** It closes the file when the block ends, even if an error is raised inside it. Without it, you have to remember to call `close()` yourself.

**What does the "w" mode do to an existing file?** It empties the file first, then writes. Use `"a"` if you want to add to the end instead.

**Why use pathlib instead of joining strings?** Separators differ between systems, and `Path` picks the right one. It also gives you `exists()`, `read_text()` and `write_text()` on the same object.

**Which Python values can JSON store?** Strings, numbers, booleans, `None`, lists and dictionaries with string keys. Other types, such as sets, need converting first.

**Why is grace missing from the file?** Adding `grace` changed the dictionary in memory only. Call `json.dump` again to save it.

This lesson follows on from [Python errors and exceptions](/articles/python/beginner/errors-and-exceptions/). Next in the series: modules and uv.
