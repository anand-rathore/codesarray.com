title: Python errors and exceptions: try, except, else, finally, raise
summary: Catch a Python error with try and except instead of crashing, run cleanup with finally, raise your own errors, and read a traceback from the bottom up.
description: Python errors and exceptions for beginners: use try, except, else and finally, raise your own error, and read a traceback without panic.
date: 2026-10-11
read: 4 min read
lesson: 10
video: Errors and exceptions | https://youtu.be/OWmknV3P8Jg
image: cover.png
---
When Python hits a problem it raises an exception, and the program stops. By the end of this page you will catch Python errors with `try` and `except` instead of crashing, run cleanup code with `finally`, raise your own errors, and read a traceback.

## try and except

Wrap the risky line in `try`, and add an `except` for the error you expect. `int("abc")` raises a `ValueError`. The `except ValueError` block catches it, and the program carries on. Always name the error you expect: a bare `except` hides real bugs, including ones you never meant to catch.

## else and finally

Two more blocks finish the picture. `else` runs only when nothing went wrong. `finally` runs every time, error or not, which makes it the place for cleanup. The order is: `try`, then `except` if it failed or `else` if it worked, and `finally` at the end either way. It runs even when the function returns from inside the `try` or `except`.

## raise and custom exceptions

You can raise errors yourself. Write `raise`, then the exception and a message, when your code finds something it cannot accept, like `raise ValueError("negative age")`. For your own kind of problem, make a custom exception: a class that inherits from `Exception`, such as `class AgeError(Exception): pass`. It gives callers one clear name to catch.

From Python 3.14 you can also list several errors after `except` without parentheses: `except ZeroDivisionError, ValueError:`. On older versions, write `except (ZeroDivisionError, ValueError):`.

## Reading a traceback

When an error is not caught, Python prints a traceback. Read it from the bottom. The last line names the error and says what went wrong. The lines above show where, from the call that started it down to the exact line that failed.

```text
Traceback (most recent call last):
  File "main.py", line 4, in <module>
    parse_age("abc")
  File "main.py", line 2, in parse_age
    return int(text)
ValueError: invalid literal for int() with base 10: 'abc'
```

## The whole program

```python
def parse_age(text):
    try:
        age = int(text)
    except ValueError:
        print("not a number")
        return None
    else:
        print("parsed")
    finally:
        print("done")
    if age < 0:
        raise ValueError("negative age")
    return age

print(parse_age("42"))
print(parse_age("abc"))
```

```output
parsed
done
42
not a number
done
None
```

Line 1 defines `parse_age`. Line 3 tries to turn the text into a number. Line 4 catches a `ValueError`, line 5 reports it, and line 6 returns `None`. Line 7 is `else`, and line 8 prints `parsed` when it worked. Line 9 is `finally`, and line 10 prints `done` every time. Line 11 checks the age, and line 12 raises an error if it is negative. Line 13 returns the age. Lines 15 and 16 call it with `"42"`, then with `"abc"`. Notice that `done` prints in both calls, even though the second one returned early.

## What you learned

- `try` wraps risky code, and `except` catches a named error.
- `else` runs when nothing went wrong, and `finally` always runs.
- `raise` signals your own error, and a class that inherits from `Exception` makes a custom one.
- A traceback reads from the bottom up: the last line says what, the lines above say where.

## Common questions

**Why not just write a bare except?** It catches everything, including typos and bugs you want to see. Name the error you expect, such as `except ValueError`, so anything else still shows up.

**Does finally run if the function returns inside try?** Yes. `finally` runs before the function actually returns, which is why it is the right place for cleanup.

**What is the difference between an error and an exception?** For everyday Python they are the same thing. An error is raised as an exception object, and `ValueError`, `KeyError` and `ZeroDivisionError` are all exceptions you can catch.

**Can I catch more than one kind of error?** Yes. Put them in a tuple: `except (ZeroDivisionError, ValueError):`. In Python 3.14 the parentheses are optional.

**Which line of a traceback should I read first?** The last one. It names the error and the message, and the lines above it lead back to the call that caused it.

This lesson follows on from [Python comprehensions](/articles/python/beginner/comprehensions/). Next in the series: files and JSON.
