title: Python closures and scope: LEGB, nonlocal and late binding
summary: Where Python looks for a name, how a function inside a function remembers its variables, how nonlocal changes them, and why lambdas made in a loop all return the same value.
description: Python closures and scope explained: the LEGB rule, inner functions that remember variables, nonlocal, and the late binding trap with lambdas in a loop.
date: 2026-10-15
read: 4 min read
lesson: 3
video: Closures and Scope in Python | https://youtu.be/ONDuUy7CDqc
image: cover.png
---
By the end of this page you will know where Python looks when it meets a name, be able to write a function that makes other functions, and understand why three lambdas made in a loop can all return the same value.

## Python scope: the LEGB rule

When Python meets a name, it looks in four places, in this order:

1. **Local**: inside the current function.
2. **Enclosing**: inside any function that surrounds it.
3. **Global**: the top level of the module.
4. **Built-in**: names like `len` and `print`.

The first match wins. People remember it as LEGB. If a function reads `x` and there is an `x` in the enclosing function and another at module level, the enclosing one is used.

## Closures: functions that make functions

A function defined inside another function can use the outer function's variables, even after the outer function has returned. The inner function carries those variables with it. That is a closure.

```python
def times(n):
    def f(x):
        return x * n
    return f

double = times(2)
triple = times(3)
print(double(5), triple(5))
```

```output
10 15
```

`double` and `triple` each remember their own `n`. `times` has finished running, but the value is still there.

## nonlocal: changing the enclosing variable

There is one catch. Assigning to a name inside a function makes that name local. So `count += 1` in an inner function fails, because `count` is not local there:

```output
UnboundLocalError: cannot access local variable 'count' where it is not associated with a value
```

Writing `nonlocal count` tells Python the name belongs to the enclosing function. Now the inner function can change it, and the change sticks between calls. Reading a name needs no keyword; only assigning does.

## Late binding: the lambda in a loop trap

A closure remembers the variable, not its value at that moment. Build three lambdas in a loop that each return `i`, and call them after the loop:

```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])
```

```output
[2, 2, 2]
```

All three share the one `i`, and by the time you call them it is 2. The fix is a default argument, which is evaluated when the lambda is made:

```python
fs = [lambda i=i: i for i in range(3)]
print([f() for f in fs])
```

```output
[0, 1, 2]
```

## The counter factory, line by line

```python
def make_counter():
    count = 0
    def tick():
        nonlocal count
        count += 1
        return count
    return tick

a = make_counter()
b = make_counter()
print(a())
print(a())
print(b())
```

`make_counter` sets `count` to zero in the enclosing scope and defines `tick` inside it. `nonlocal count` lets `tick` change that variable, then `tick` adds one and returns it. The last line of `make_counter` returns `tick` itself, without calling it. Lines 9 and 10 make two separate counters. `a` is called twice and `b` once.

```output
1
2
1
```

`a` remembers its count between calls, so it prints 1 then 2. `b` has its own `count`, separate from `a`, so it starts again at 1.

## What you learned

- Python looks up names local, enclosing, global, then built-in, and the first match wins.
- A function inside a function is a closure, and it remembers the variables around it.
- `nonlocal` lets the inner function change an enclosing variable.
- Closures keep the variable, not the value, so lambdas in a loop share one `i`.
- A default argument such as `lambda i=i: i` captures the value at that moment.

## Common questions

**What is the difference between `global` and `nonlocal`?** `global x` points a name at the module-level variable. `nonlocal x` points it at the nearest enclosing function's variable. Both are only needed when you assign; reading works without them.

**Why do I get UnboundLocalError?** Somewhere in the function you assign to that name, which makes it local for the whole function. Reading it before the assignment then fails. Use `nonlocal` or `global` if you meant the outer variable, or pass the value in as an argument.

**Does a closure copy the variable?** No. It keeps a reference to the variable itself, so if the outer variable changes before you call the inner function, you see the new value. That is the cause of the late binding trap.

**Can I see what a closure remembers?** Yes. For the `times` example, `double.__code__.co_freevars` is `('n',)` and `double.__closure__[0].cell_contents` is `2`.

**When should I use a closure instead of a class?** When you need one small piece of remembered state and one action, like a counter or a configured function. When there are several actions or the state grows, a class is clearer.

Next in the series: decorators, and how to wrap a function without touching its code.
