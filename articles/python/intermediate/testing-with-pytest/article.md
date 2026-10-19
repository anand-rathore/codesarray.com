title: Python testing with pytest: write and run tests
summary: How to test Python code with pytest: how it finds tests by name, how a test is a plain assert, what a failure shows, and how to run one test on many inputs with parametrize. One short test file with its real output.
description: Python testing with pytest explained: test discovery by name, a plain assert, reading a failure, and pytest.mark.parametrize, with real output.
date: 2026-10-19
read: 4 min read
lesson: 16
video: Python Testing with pytest: Write and Run Tests | https://youtu.be/0FMjE920Egk
image: cover.png
---
By the end of this page you will know how to test Python code with pytest: how it finds your tests, how to write one with a plain `assert`, what a failing test shows you, and how to run one test on many inputs. It builds on [Python functions](/articles/python/beginner/functions/), because a test is a function that calls your own.

## How pytest finds tests

Pytest finds tests by name. It looks for files that start with `test_`, and inside them, functions that start with `test`. Run `pytest` in your project folder and it collects every one and runs it. A function with any other name, like `add`, is just ignored, so you can keep helpers and real code in the same file.

## A test is a plain assert

A test is a function with a plain `assert`. If the expression is true, the test passes. If it is false, the test fails, and pytest shows you both sides of the comparison. If `add(2, 3)` came out as 5 but the test expected 6, pytest prints:

```output
>       assert add(2, 3) == 6
E       assert 5 == 6
E        +  where 5 = add(2, 3)
```

There is no special assertion method to learn. You write the check the way you would say it.

## Run one test on many inputs

`pytest.mark.parametrize` runs one test with many inputs. You give it the names of the arguments and a list of cases. Pytest runs the function once for each case and counts each as its own test. Add a case to the list and you get another test, without writing another function.

## The code

```python
import pytest


def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5


@pytest.mark.parametrize("a, b, total", [(0, 0, 0), (-1, 1, 0)])
def test_add_more(a, b, total):
    assert add(a, b) == total
```

Save it as `test_add.py` and run `pytest`:

```output
test_add.py ...
3 passed in 0.10s
```

Pytest prints a few more lines around these, and the time will differ on your machine. Each dot is one passing test. There are three: the plain test, and the two parametrize cases.

## The code line by line

- Line 1 imports `pytest`, which `parametrize` needs.
- Lines 4 and 5 define `add`, the function we are testing.
- Lines 8 and 9 are the first test. It asserts that `add(2, 3)` is 5.
- Line 12 lists two cases for the `parametrize` decorator: `(0, 0, 0)` and `(-1, 1, 0)`.
- Lines 13 and 14 are one test that runs once for each case, and asserts the total.

## What you learned

- Pytest finds files that start with `test_` and functions that start with `test`.
- A test is a function with a plain `assert`.
- When an assert fails, pytest shows both sides.
- `@pytest.mark.parametrize` runs one test on many inputs.
- A dot in the output means a test passed.

## Common questions

**How do I install pytest?** It is not part of the standard library. In a uv project run `uv add --dev pytest`, or use `pip install pytest` in an environment you made yourself. Then `pytest` runs from the project folder.

**What if pytest says no tests ran?** Check the names. A file called `check_add.py` is not collected, and neither is a function called `check_add`. Rename them to start with `test_` and `test`.

**How do I run just one test?** Give the file and the function name: `pytest test_add.py::test_add` runs only that test. `pytest -k more` runs every test with `more` in its name, which here is the two parametrize cases.

**How do I check that code raises an error?** Use `pytest.raises` as a `with` block: `with pytest.raises(ZeroDivisionError): 1 / 0`. The test passes only if that error is raised inside the block.

**How do I see each test by name?** Run `pytest -v`. Each parametrize case gets its own line, such as `test_add.py::test_add_more[-1-1-0] PASSED`.

Next in the series: packaging with uv.
