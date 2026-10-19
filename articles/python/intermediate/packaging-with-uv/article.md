title: Python packaging with uv: build and publish a package
summary: How to package Python code with uv: start a package with uv init, name a command in pyproject.toml, build a wheel with uv build, and publish it to PyPI. One small function with its real output.
description: Python packaging with uv explained: uv init --package, the pyproject.toml scripts table, uv build for a wheel, and uv publish, with real output.
date: 2026-10-19
read: 4 min read
lesson: 17
video: Python Packaging with uv: Build and Publish a Package | https://youtu.be/iwxg14e4ro4
image: cover.png
---
By the end of this page you will know how to package Python code with uv: how to start a package, how a command gets its name from the project file, and how to build a wheel you can share. It builds on [Python modules and uv](/articles/python/beginner/modules-and-uv/), where you first met `pyproject.toml`.

## Start a package

Run `uv init --package greet`. Uv makes a folder with two things. A `pyproject.toml` file, which describes the project, and a `src` folder with your code inside a folder named `greet`. That layout, a source folder holding a folder with the package name, is what makes it a package.

## Name a command with an entry point

The project file can also name a command. It looks like this:

```toml
[project.scripts]
greet = "greet:main"
```

This means: when someone types `greet`, call the function `main` in the `greet` package. That is called an entry point. Uv writes this table for you when you use `--package`.

## Build a wheel and publish it

Run `uv build`. It writes two files into a `dist` folder:

```output
Successfully built dist\greet-0.1.0.tar.gz
Successfully built dist\greet-0.1.0-py3-none-any.whl
```

The wheel, the `.whl` file, is what people install. The `.tar.gz` is a copy of the source. Then `uv publish` uploads both to PyPI, the place that `pip` and `uv` install from. You need an account on PyPI and an API token to prove the package is yours, so it is the one step this page does not run.

## The code

This is the code inside the package, in `src/greet/__init__.py`:

```python
import sys


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "world"
    print(f"Hello, {name}!")
```

Run it with `uv run greet Ada`:

```output
Hello, Ada!
```

Type `uv run greet` with no name and it prints `Hello, world!`.

## The code line by line

- Line 1 imports `sys`, which holds the words typed after the command.
- Line 4 defines `main`, the function the entry point calls.
- Line 5 takes the name you typed after the command, or `world` if you typed nothing.
- Line 6 prints the greeting.

## What you learned

- `uv init --package` starts a package with a `pyproject.toml` and a `src` folder.
- The `[project.scripts]` table names a command and the function it calls.
- `uv build` makes a wheel and a source copy in `dist`.
- `uv publish` uploads them to PyPI with a token.

## Common questions

**What is a wheel?** A wheel is a ready-to-install file with the extension `.whl`. Installing it is quick because nothing has to be built on the user's machine.

**What is the difference between a package and a module?** A module is one Python file. A package is a folder of modules that you install and import by name.

**Do I need uv to build a package?** No. The `[build-system]` table in `pyproject.toml` names the build tool, and `python -m build` works with the same file. Uv is just the fastest way to run the steps.

**Can I try publishing without the real PyPI?** Yes. PyPI has a test site, and `uv publish --publish-url https://test.pypi.org/legacy/` uploads there. Check the name is free first, because a published version can never be replaced.

**How do I change the version?** Edit `version` in `pyproject.toml`, then run `uv build` again. PyPI refuses an upload of a version number that already exists.

Next in the series: graphs, BFS and DFS.
