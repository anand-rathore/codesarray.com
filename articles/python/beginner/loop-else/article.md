title: Python for else: the else that means no break
summary: A Python for loop can have an else block, and it does not mean what you think. It runs only when the loop finished on its own, with no break.
description: Python for else explained: the else block on a for or while loop runs only when the loop finished without a break, which replaces the usual flag variable in a search.
date: 2026-10-07
read: 2 min read
follows: 3
video: The else on a loop | https://youtube.com/shorts/VLexBB4ZSHA
image: cover.png
---
A Python for loop can have an else. It does not mean what you think: the else belongs to the loop, not to the if inside it, and it runs only when the loop finished on its own, with no `break`. The usual job for it is a search.

## break fires, the else is skipped

```python
colors = ["red", "green", "blue"]
for word in colors:
    if word == "green":
        print("found", word)
        break
else:
    print("not found")
```

```output
found green
```

The loop finds `green`, prints it and breaks. Because a `break` ended the loop, the `else` block does not run.

## No break, the else runs

Change the search to a colour that is not in the list:

```python
colors = ["red", "green", "blue"]
for word in colors:
    if word == "pink":
        print("found", word)
        break
else:
    print("not found")
```

```output
not found
```

The loop runs out of words without ever breaking, so the `else` runs. Without this feature you would set a flag variable to `False` before the loop, set it to `True` when you find the item, and test it after the loop. The loop's `else` does all of that in one word.

## Read it as "no break"

The confusing part is the name. Think of it as `nobreak:` and it reads correctly: the block after the loop that runs when no `break` happened. A `while` loop can have one too, with the same rule: the `else` runs when the condition became `False` on its own, and is skipped when a `break` ended the loop.

## What to take from this

- `for ... else:` runs the `else` block only when the loop finished with no `break`.
- It belongs to the loop, not to the `if` inside it.
- Use it to say "the search failed" without a flag variable.

This is a short note on [Control flow](/articles/python/beginner/control-flow/), lesson 3 of the Python beginner track.
