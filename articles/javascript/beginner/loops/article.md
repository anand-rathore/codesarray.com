title: JavaScript loops: for, while, for...of, break and continue
summary: How your code repeats itself: the three parts of every loop, while, do while, for, break and continue, for...of for lists and strings, why for...in is the wrong loop for an array, nested loops and a labeled break. Three short programs with their real output.
description: JavaScript loops for beginners: while, do while, for, for...of, break and continue, nested loops with a labeled break, and why for...in is wrong for arrays.
date: 2026-11-06
read: 10 min read
lesson: 6
video: Loops | https://youtu.be/C4Xc1mRCR8s
image: cover.png
---
This lesson is about JavaScript loops: how your code repeats itself. By the end of this page you will write a `while` loop and a `do...while` loop, count with a `for` loop, walk through values with `for...of`, stop early with `break`, skip a round with `continue`, and escape two loops at once with a label. You will also know why `for...in` is the wrong tool for a list.

## Why loops, and the three parts

Picture a barista who has to make a hundred coffees. They do not invent a new method a hundred times: they do the same steps again and again. That is a loop. You write the steps once and run them as many times as you need.

Every loop has the same three parts: a starting point, a question that decides "should we go round again?", and a step that moves us forward. If you forget the step, the question never changes and the loop never ends. That is an infinite loop, and it is the most common loop mistake.

## while

The simplest loop is `while`. Think of a kettle: while the water is cold, keep heating. Write `while`, the question in round brackets, then curly braces with the code to repeat. Before every round JavaScript asks the question. If it is truthy the code runs and it asks again, and if it is falsy the loop is over.

With `let n = 3`, the loop `while (n > 0)` prints `brewing 3`, then `n--` takes one off, and so on until `n` is `0`. The starting point is above the loop and the step is inside it. Take away `n--` and `n` stays `3` forever.

## do...while

A `while` loop might never run at all: if the question is false at the start, JavaScript skips it. When you want the code to run at least once, like a free taste before the customer decides, use `do...while`. You write `do`, the code in curly braces, and then `while` with the question at the end.

The question comes after the code, so the code always runs once. With `sugar` at `0`, the loop prints `taste once`, asks "is sugar greater than 0?", gets no, and stops. A normal `while` with the same question would have run zero times.

## for

Most of the time you know how many rounds you need, and that is what the `for` loop is for. Picture a clipboard with a counter: start at one, stop after five, add one each time. A `for` loop puts all three parts in one line, in round brackets split by semicolons:

- `let i = 1` is the start. It runs once, before the loop begins.
- `i <= 5` is the question. It is asked before every round.
- `i++` is the step. It runs after every round.

Use `let` for `i`, never `const`, because `i` has to change. To count down, start at the top and use `i--`. Watch out for off by one mistakes: `i < 5` gives four rounds, `i <= 5` gives five.

## break and continue

You can change a loop while it is running. `break` stops the whole loop right now, like a barista who runs out of milk and closes the shop. `continue` skips the rest of this round and goes straight to the next one, like crossing out an order and moving on.

In the program below, `i` goes from 1 to 5. When `i` is `2`, `continue` skips it. When `i` is `4`, `break` ends the loop, so orders 4 and 5 never happen. You see `order 1` and `order 3`. Both work in `while` and `do...while` loops too.

## for...of

When you just want every item in something, use `for...of`. Picture a stack of order slips: you pick one up, read it, put it down and take the next. You do not care about the position. Write `for (const drink of drinks)` and each round `drink` holds the next item: `"latte"`, then `"mocha"`. There is no counter, no question and no step, so there are no off by one mistakes. Use `const`, because each round gets a brand new `drink`.

`for...of` also works on strings. Loop over `"cafe"` and you get `c`, `a`, `f`, `e`, one letter at a time. If you put each new letter in front of what you have so far, `"cafe"` becomes `"efac"`. If you need the position as well as the value, use a normal `for` loop. For everything else, `for...of` is the neat choice.

## for...in

A close cousin has a confusing name: `for...in`. `for...of` gives you the values, `for...in` gives you the keys. Think of a row of numbered cups: `for...of` reads the drink inside, `for...in` reads the number printed on the cup.

Loop over the two drinks with `for...in` and you get `0` and `1`, not `latte` and `mocha`. Worse, those keys are strings: the string `"0"` and the string `"1"`, not numbers. Add `1` to that key and you get the string `"01"`, not `1`. That is why `for...in` is the wrong tool for a list. It is made for objects, where the keys are names, and we meet objects in video 10. For now: lists and strings, use `for...of`; counting, use `for`.

## Nested loops and a labeled break

Loops can live inside loops. A cafe has tables, and every table has seats: the outer loop picks a table, and for every round of it the inner loop runs all the way through the seats. Three tables with three seats is nine rounds.

Now say a fire alarm goes off at table 2, seat 2, and you want to leave everything. A plain `break` only leaves the loop it is in, so it would stop the seats and carry on to table 3. The fix is a label: put a name and a colon in front of the outer loop, `outer:`, then write `break outer`. JavaScript leaves both loops at once. Use it rarely, for example when searching a grid and quitting the moment you find what you want.

## Four common loop mistakes

1. **The infinite loop.** You forgot the step, so the question is always true. If your program freezes, check this first.
2. **Off by one.** `<` versus `<=`. Say the rounds out loud.
3. **`const` for the counter.** `for (const i = 0; i < 3; i++)` breaks on the first step, because `const` cannot change.
4. **`for...in` on a list.** You get strings, not items.

## The cafe loops program

```javascript
// a cafe serves orders in a loop
let n = 3;
while (n > 0) {
  console.log("brewing", n);
  n--;
}

let sugar = 0;
do {
  console.log("taste once");
} while (sugar > 0);

for (let i = 1; i <= 5; i++) {
  if (i === 2) continue;
  if (i === 4) break;
  console.log("order", i);
}
```

```output
brewing 3
brewing 2
brewing 1
taste once
order 1
order 3
```

Lines 2 to 6 are the `while` loop: `n` starts at 3, line 4 prints, and line 5 takes one off so the loop can end. Lines 8 to 11 are the `do...while`: `sugar` is `0`, line 10 prints `taste once`, and the question on line 11 is false, so it stops after one round. Lines 13 to 17 are the `for` loop: line 14 skips order 2 with `continue`, line 15 stops everything at 4 with `break`, and line 16 prints the order number.

## The for...of and for...in program

```javascript
// for...of walks values, for...in walks keys
const drinks = ["latte", "mocha"];
for (const drink of drinks) {
  console.log(drink.toUpperCase());
}

let reversed = "";
for (const ch of "cafe") {
  reversed = ch + reversed;
}
console.log(reversed);

for (const key in drinks) {
  console.log(key, typeof key);
}
```

```output
LATTE
MOCHA
efac
0 string
1 string
```

Line 3 is `for...of`: each round `drink` holds the next item, and line 4 prints it in capital letters. Lines 7 to 11 loop over each letter of `"cafe"`, put the new letter in front of what we have, and print `efac`. Line 13 is `for...in` on the same list, and it prints each key with its type: `0 string` and `1 string`.

## The tables and seats program

```javascript
// tables and seats: a loop inside a loop
outer: for (let table = 1; table <= 3; table++) {
  for (let seat = 1; seat <= 3; seat++) {
    if (table === 2 && seat === 2) break outer;
    console.log("table", table, "seat", seat);
  }
}
console.log("closed");
```

```output
table 1 seat 1
table 1 seat 2
table 1 seat 3
table 2 seat 1
closed
```

Line 2 is the outer loop with its label `outer`, and line 3 is the inner loop over the seats. Line 4 is the alarm: at table 2, seat 2, `break outer` leaves both loops. So table 2 seat 2 is never printed, table 3 never starts, and line 8 prints `closed`.

## What you learned

- Every loop has a start, a question and a step. No step means an infinite loop.
- `while` asks the question first. `do...while` runs the code once and then asks.
- `for` puts the start, the question and the step in one line.
- `break` stops the loop and `continue` skips to the next round.
- `for...of` walks the values of a list or a string. `for...in` walks keys as strings, so keep it for objects.
- A label lets `break` leave a loop inside a loop.

## Common questions

**What is the difference between `for...of` and `for...in` in JavaScript?** `for...of` gives you each value of an array or a string. `for...in` gives you the keys, and they are strings, so for an array you get `"0"` and `"1"` instead of the items. Use `for...of` for lists and keep `for...in` for objects.

**Why is my JavaScript loop never ending?** Almost always the step is missing, so the question stays true. Check that something inside the loop changes the thing the question looks at, like `n--` or `i++`.

**What is the difference between `while` and `do...while`?** `while` asks the question before the first round, so it can run zero times. `do...while` runs the code once and asks afterwards, so it always runs at least once.

**What does `break` do and how is it different from `continue`?** `break` stops the whole loop. `continue` skips only the rest of the current round and goes on with the next one.

**How do I break out of two loops at once?** Put a label in front of the outer loop, like `outer:`, and write `break outer` inside the inner loop.

**Can I use `const` in a `for` loop?** Not for the counter: `for (let i = 0; i < 3; i++)` needs `let` because `i` changes. In `for...of` you can use `const`, because each round gets a new variable.

Next in the series: functions.
