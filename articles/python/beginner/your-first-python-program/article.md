title: Your first Python program
summary: Install Python 3.14, run it two ways, and read an eleven-line program one line at a time.
date: 2026-10-02
read: 4 min read
lesson: 1
video: Hello, Python | https://youtu.be/NExcPTw_LvQ
aliases: /articles/your-first-python-program/
---
By the end of this page you will have Python installed, you will have run a program two different ways, and you will know the one rule that makes Python look different from every other language.

## Install it

Go to [python.org](https://www.python.org/downloads/) and download Python 3.14. On Windows, tick the box that says **Add Python to PATH** before you click install. Without it, the terminal will not know what `python` means.

Then open a terminal and check:

```
python --version
```

```output
Python 3.14.7
```

If you see a version that starts with 3.14, you are ready.

## Two ways to run Python

The first is the REPL, the interactive shell. Type `python` on its own and press enter. You get a prompt with three angle brackets, and Python answers each line as soon as you type it:

```
>>> 2 + 3
5
```

The REPL is for experimenting. Since 3.14 it even colours your code as you type.

The second way is a file. Save your code as `hello.py` and run it with:

```
python hello.py
```

Files are for programs you want to keep and run again. Everything in this series lives in files.

## The program

```python
# my first Python program
print("Hello, World!")

name = "Ada"
print("Hello,", name)

age = 36
if age >= 18:
    print(name, "is an adult")
    print("Welcome aboard")
print("Done")
```

Line by line:

- **Line 1** is a comment. Anything after a `#` is ignored by Python; it is a note for humans.
- **Line 2** calls `print`, the function that shows text on screen.
- **Line 4** stores the text `"Ada"` in a variable called `name`.
- **Line 5** prints two things at once. `print` puts a space between them.
- **Line 7** stores a number.
- **Line 8** asks a question: is `age` at least 18?
- **Lines 9 and 10** run only if the answer is yes.
- **Line 11** always runs.

## The rule: indentation is the code

Python has no curly braces. The lines that belong to the `if` are the ones indented underneath it. Four spaces is the convention. The moment you go back to the left margin, you are outside the block.

If you forget to indent, Python refuses to run the file:

```output
IndentationError: expected an indented block after 'if' statement on line 2
```

In Python, the whitespace is the code.

## Run it

Python reads the file from top to bottom:

```output
Hello, World!
Hello, Ada
Ada is an adult
Welcome aboard
Done
```

Because 36 is at least 18, both lines inside the `if` run, and then `Done`.

## What you learned

- `python --version` checks your install.
- `python` on its own opens the REPL.
- `python hello.py` runs a file.
- `print(...)` shows output.
- `#` starts a comment.
- Four spaces of indentation make a block.

Next in the series: variables and types.
