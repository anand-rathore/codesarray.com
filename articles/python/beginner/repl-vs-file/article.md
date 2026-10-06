title: Python REPL vs .py file: two ways to run Python
summary: When to type into the interactive shell, when to save a file, and what Python 3.14 added to the shell.
description: The difference between the Python REPL (interactive shell) and running a .py file, when to use each, and the syntax colouring added in Python 3.14.
date: 2026-10-05
read: 2 min read
follows: 1
video: Run Python one line at a time | https://youtube.com/shorts/7aIQ590QE34
image: cover.png
aliases: /articles/python-repl-vs-file/
---
There are two ways to run Python code, and beginners usually only know one. You can type into the Python REPL, the interactive shell, and get an answer after each line, or you can save your code in a `.py` file and run the whole thing.

## The REPL: ask, get an answer

Type `python` in a terminal and press enter. You get the REPL, the interactive shell, with a `>>>` prompt:

```
> python
>>> 40 * 0.2
8.0
>>> price = 40
>>> price + price * 0.2
48.0
```

Each line runs the moment you press enter. Ask it forty times zero point two, and it answers `8.0` straight away. Store a price, use it on the next line, and you get `48.0`. No file, and no run button.

Since Python 3.14 the shell also colours your code as you type, the way an editor does.

The catch: close the window and everything is gone. The REPL remembers `price` only for as long as it is open.

## A file: keep it, run it again

Put the same three lines in a file called `total.py`:

```python
price = 40
tax = price * 0.2
print("total:", price + tax)
```

Run it with:

```
python total.py
```

```output
total: 48.0
```

Same answer, and this time you keep it. You can run it again tomorrow, change one number, or send it to someone.

Notice the `print`. The REPL shows the value of every line for you. A file shows only what you print.

## Which one to use

- Use the **REPL** to experiment: check what a function returns, try an expression, test an idea in ten seconds.
- Use a **file** for anything you want to keep, run again, or build on.

REPL to experiment, file to keep.

Both are covered step by step in [Your first Python program](/articles/python/beginner/your-first-python-program/).
