title: Python template strings: t-strings in 3.14, Template and Interpolation
summary: How a t-string differs from an f-string, what a Template object holds, and how to write a processor that escapes HTML or turns a query into placeholders. Three short programs with their real output.
description: Python template strings (t-strings, new in 3.14): what a Template and an Interpolation hold, and how to write safe HTML and SQL processors, with real code and output.
date: 2026-10-31
read: 8 min read
lesson: 13
video: Python template strings | https://youtu.be/AEocoIgrMLY
image: cover.png
---
By the end of this page you will know what a Python template string (a t-string) returns, what a `Template` object holds, why that makes HTML and SQL safer, and how to write your own processor. A t-string looks almost exactly like an f-string, with a `t` in front instead of an `f`, but an f-string gives you finished text and a t-string gives you the pieces. t-strings are new in Python 3.14. It follows [Python context managers and protocols](/articles/python/advanced/context-managers-and-protocols/).

## The problem: values merged into text

Say you build a query with an f-string and put a user name inside. The moment the f-string runs, the name is merged into the text, and the database cannot tell your SQL from the user's input. If the name contains a quote and a bit of SQL, that is an injection attack. The same happens with HTML, where a comment can carry a script tag. Escaping by hand works only if you never forget. A t-string keeps the user's value separate from your text, so a function can handle it safely.

## f-string versus t-string

An f-string is evaluated right away and returns a plain `str`. Whatever was in the braces is already pasted in, and the information about where it came from is gone. A t-string is also evaluated right away, but it does not build a string. It returns a `Template` object that remembers the fixed text pieces and the values that were in the braces, each one kept apart. Nothing is joined and nothing is escaped. That decision is left to you.

## What a Template holds

A `Template` has two tuples. `strings` holds the fixed text pieces between the braces. `interpolations` holds one `Interpolation` object for each brace. There is always one more string than interpolations, because text surrounds every brace, even if that text is empty. Each `Interpolation` has four fields:

- `value`: the result of the expression.
- `expression`: the source text, like `name`.
- `conversion`: `"r"`, `"s"` or `"a"` for `!r`, `!s` or `!a`, or `None`.
- `format_spec`: whatever came after the colon.

```python
name = "Ada"
tmpl = t"Hi {name}, you are {3 * 14:>4}!"
print(type(tmpl).__name__)
print(tmpl.strings)
print(tmpl.values)
item = tmpl.interpolations[0]
print(item.expression, item.value, item.conversion)
print(tmpl.interpolations[1].format_spec)
print(type(f"{name}").__name__)
```

Output:

```output
Template
('Hi ', ', you are ', '!')
('Ada', 42)
name Ada None
>4
str
```

The type is `Template`, not `str`. The strings are `'Hi '`, `', you are '` and `'!'`: three pieces for two braces. The values are `'Ada'` and `42`, already computed. For the first interpolation the expression is `name`, the value is `Ada` and the conversion is `None`. The format spec of the second is `>4`. And the f-string is just `str`: the t-string kept everything the f-string threw away.

## Looping over a Template

You can loop over a `Template`. It gives you the pieces in order: a string, then an `Interpolation`, then a string, skipping any empty strings. That is the shape almost every processor uses. For each piece, ask whether it is an `Interpolation`. If so, treat the value with care. If not, it is your own trusted text, so keep it as it is. Calling `str()` on a `Template` does not join anything: a `Template` is not a string, and joining is your job.

## What t-strings are for

Processors are good for escaping HTML, building SQL with placeholders so the database receives the values separately, safe shell commands, structured logging that keeps values as fields, and small languages. t-strings are not a replacement for f-strings: if you just want text, keep using f-strings. And Python does not ship a processor for you. You write the function, or use a library that did.

## An HTML processor

```python
from html import escape
from string.templatelib import Template, Interpolation

def render_html(template: Template) -> str:
    parts = []
    for item in template:
        if isinstance(item, Interpolation):
            parts.append(escape(str(item.value)))
        else:
            parts.append(item)
    return "".join(parts)

comment = "<script>alert(1)</script>"
page = t"<p>{comment}</p>"
print(render_html(page))
print(render_html(t"<p>{'fine'}</p>"))
print(render_html(t"<p></p>"))
```

Output:

```output
<p>&lt;script&gt;alert(1)&lt;/script&gt;</p>
<p>fine</p>
<p></p>
```

`render_html` loops over the template. An `Interpolation` has its value turned into a string and escaped with `html.escape`; anything else is your own text and is kept as it is. The script tag comes out as `&lt;script&gt;`, which a browser shows as text instead of running it. The safe value is unchanged, and a template with no braces still works. You never had to remember to escape: the processor does it for every brace, and the `<p>` tags you wrote yourself were left alone.

## A SQL processor

```python
from string.templatelib import Template, Interpolation

def to_sql(template: Template) -> tuple[str, list]:
    query, params = [], []
    for item in template:
        if isinstance(item, Interpolation):
            query.append("?")
            params.append(item.value)
        else:
            query.append(item)
    return "".join(query), params

user = "x' OR '1'='1"
age = 30
sql, params = to_sql(t"SELECT * FROM users WHERE name = {user} AND age > {age}")
print(sql)
print(params)
print(to_sql(t"SELECT 1"))
```

Output:

```output
SELECT * FROM users WHERE name = ? AND age > ?
["x' OR '1'='1", 30]
('SELECT 1', [])
```

Each `Interpolation` adds a `?` placeholder to the query and its value to `params`; everything else is your SQL text. The hostile name never touches the query text: it sits in the parameter list, whole, as one value. A database driver takes the query and the list separately, so the quote is just a character, not SQL. A template with no braces gives `SELECT 1` and an empty list. This is the same protection as a hand written parameterised query, with the readable syntax of an f-string.

## Common mistakes

- A t-string needs Python 3.14 or later; an older Python gives a `SyntaxError`.
- Do not call `str()` on a `Template` and expect text.
- Do not join the pieces without checking for `Interpolation` first, or you are back to an f-string.
- A processor has to handle conversions and format specs if you want to honour them.
- A t-string is only safe if the function that receives it is. The syntax gives you the pieces; the safety comes from what you do with them.

## What you learned

- A t-string returns a `Template`, not a `str`.
- A `Template` has `strings` and `interpolations`, and each `Interpolation` has `value`, `expression`, `conversion` and `format_spec`.
- Loop over a `Template`, treat each `Interpolation` with care and keep the rest as it is.
- Use it for HTML, SQL and anywhere user input meets your text, and keep f-strings for plain text.

## Common questions

**What is a t-string in Python?** A template string, written with a `t` before the quote, new in Python 3.14. It looks like an f-string but returns a `Template` object that keeps the text pieces and the values apart instead of a joined string.

**What is the difference between a t-string and an f-string?** An f-string returns a `str` with the values already pasted in. A t-string returns a `Template` with `strings` and `interpolations`, so a function can decide how each value is handled before anything is joined.

**Does str() work on a Template?** It returns a description of the object, not the joined text. Joining is the job of your processor.

**Do t-strings make my SQL safe by themselves?** No. The `Template` only gives you the pieces. The safety comes from a processor like `to_sql` that sends the values as parameters and never pastes them into the query.

**What is in an Interpolation?** Four fields: `value` (the result), `expression` (the source text), `conversion` (`r`, `s`, `a` or `None`) and `format_spec` (what came after the colon).

The advanced track continues in the next video.
