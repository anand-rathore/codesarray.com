title: Big O notation in JavaScript: count steps, spot the hidden loop
summary: Learn Big O notation in JavaScript by counting steps instead of seconds. Meet O(1), O(log n), O(n), O(n log n) and O(n²), see which array methods hide a loop, and fix a slow includes loop with a Set, with real output from Node.
description: Big O notation in JavaScript explained with real step counts and timings in Node: the five shapes, the hidden loop in includes, and the Set fix.
date: 2026-11-22
read: 8 min read
lesson: 1
video: Big O in JavaScript | https://youtu.be/lKjmFWEgO1w
image: cover.png
---
Big O notation in JavaScript is a way to tell, before you run anything, whether code will stay fast or fall apart as the data grows. By the end of this page you will count steps instead of seconds, recognise the five shapes you meet every day, know which JavaScript methods hide a loop, and be able to fix a loop that takes almost a second on 40,000 items. Everything here ran on Node 24.

## Why timing is not enough

The obvious check is to run the code and time it. `console.time("loop")` starts a stopwatch and `console.timeEnd("loop")` prints it, and `performance.now()` gives the time in milliseconds so you can subtract two readings. Both are useful, and we use one below. But the answer depends on your computer and on what else is running, and it only covers the input you tried. It says nothing about what happens with ten times more data.

## Count steps, not seconds

Instead, count steps. A step is one small piece of work: read an item, compare two values, add one to a total. Steps do not change when the computer changes. Then ask one question: if the input gets bigger, how does the number of steps grow? The size of the input is called `n`, and Big O is the short way to write the answer. It does not say how fast your code is. It says how the work grows.

## The five shapes

**O(1), constant.** A hallway of numbered lockers: open locker forty and you walk straight to it, whether there are fifty lockers or fifty thousand. Reading an array by index, `push`, and `get`, `set`, `has` and `add` on a `Map` or `Set` are all constant.

**O(n), linear.** Looking for one word by reading every page. A book twice as thick takes twice as long. Any loop that touches each item once is linear, and so are `includes`, `indexOf`, `find`, `map`, `filter` and `reduce`, because they walk the list for you.

**O(n²), quadratic.** A party where everyone shakes everyone else's hand. Ten people make 45 handshakes. Twenty people make 190, not 90: twice the people, four times the handshakes. In code this is a loop inside a loop.

**O(log n), logarithmic.** Guessing a number from one to a thousand. Each guess throws away half the numbers, so a thousand items need about ten steps and a million need about twenty. The catch is that the data must already be in order. This is binary search.

**O(n log n).** The cost of sorting. It sits between linear and quadratic, and `sort` and `toSorted` belong here.

## Three rules for writing it

Drop the constants: a function that loops twice is 2n, and we still call it O(n), because the shape matters, not two or three times. Keep only the biggest part: n plus n squared is O(n²), since the square swamps the rest when n is big. And count the worst case: if the item you search for is last, or missing, that is the case to plan for.

## Hidden loops

The trap in JavaScript is that one line can hide a whole loop. `includes`, `indexOf`, `find` and `slice` each walk the array. The spread syntax copies every item. `shift` has to move every other item along, while `pop` just drops the last one, so `pop` is O(1) and `shift` is O(n). Put one of these inside a loop that runs n times and you have n times n: quadratic, and you never wrote a second `for`.

## Counting steps in real code

This script keeps a `steps` counter and runs three functions on lists of 10, 100 and 1,000 items.

```js
let steps = 0;

function first(items) {
  steps++;
  return items[0];
}

function total(items) {
  let sum = 0;
  for (const n of items) {
    steps++;
    sum += n;
  }
  return sum;
}

function hasPair(items) {
  for (let i = 0; i < items.length; i++) {
    for (let j = i + 1; j < items.length; j++) {
      steps++;
      if (items[i] === items[j]) return true;
    }
  }
  return false;
}

function count(fn, items) {
  steps = 0;
  fn(items);
  return steps;
}

for (const size of [10, 100, 1000]) {
  const items = Array.from({ length: size }, (_, i) => i);
  console.log(size, count(first, items), count(total, items), count(hasPair, items));
}
```

`first` adds one step and returns the first item. `total` loops over the items and counts one step each. `hasPair` has a loop inside a loop, so it counts a step for every pair it compares. The `count` helper resets the counter, calls the function and returns the steps.

```output
10 1 10 45
100 1 100 4950
1000 1 1000 499500
```

Read down the columns. The first never moves: constant. The second grows with n, ten times the items and ten times the steps: linear. The third explodes, ten times the items and a hundred times the steps: quadratic. The 45 in the first row is the ten people at the party. There is no stopwatch and no noise, and any computer gives the same answer.

## Binary search: the flat one

Binary search keeps two pointers, `low` and `high`, finds the middle, and throws away the half that cannot hold the target.

```js
function search(sorted, target) {
  let steps = 0;
  let low = 0;
  let high = sorted.length - 1;
  while (low <= high) {
    steps++;
    const mid = Math.floor((low + high) / 2);
    if (sorted[mid] === target) break;
    if (sorted[mid] < target) low = mid + 1;
    else high = mid - 1;
  }
  return steps;
}

for (const size of [10, 1000, 1000000]) {
  const sorted = Array.from({ length: size }, (_, i) => i);
  console.log(size, search(sorted, -1));
}
```

We search for `-1`, which is not in the list, so the search goes all the way: the worst case.

```output
10 3
1000 9
1000000 19
```

Ten items took 3 steps, a thousand took 9, and a million took only 19. Double the data and you add about one step.

## The loop from the start

Here is a function that finds out whether a list has a duplicate, written two ways. `slow` keeps the values seen so far in an array and asks `includes`. `fast` keeps them in a `Set` and asks `has`.

```js
function slow(items) {
  const seen = [];
  for (const x of items) {
    if (seen.includes(x)) return true;
    seen.push(x);
  }
  return false;
}

function fast(items) {
  const seen = new Set();
  for (const x of items) {
    if (seen.has(x)) return true;
    seen.add(x);
  }
  return false;
}

function time(label, fn, items) {
  const start = performance.now();
  fn(items);
  const ms = performance.now() - start;
  console.log(label, items.length, ms.toFixed(1) + " ms");
}

for (const n of [10000, 20000, 40000]) {
  const items = Array.from({ length: n }, (_, i) => i);
  time("includes", slow, items);
  time("set", fast, items);
}
```

`slow` reads clean, but `seen.includes(x)` walks the whole of `seen` every time, so the loop is quadratic. The lists have no duplicates, so every call goes all the way. These timings are from one run, and yours will differ; the shape will not.

```output
includes 10000 98.9 ms
set 10000 1.6 ms
includes 20000 336.1 ms
set 20000 2.3 ms
includes 40000 882.9 ms
set 40000 4.8 ms
```

Each time the items double, `includes` gets several times slower, which is the quadratic shape showing up on a stopwatch. The `Set` barely moves. Same answer, about two hundred times faster at 40,000 items, from swapping an array for a `Set`.

## Things to keep in mind

- Big O is about growth. For ten items nothing here matters, and a quadratic loop over fifty items is fine.
- A better Big O is not always faster on small input. A `Set` has setup costs, and for tiny lists `includes` can win.
- Do not guess where your program is slow. Reasoning tells you what could go wrong, and measuring tells you what did.
- Watch for the hidden loop: `includes`, `indexOf`, `find` or a spread inside another loop is the moment to ask how big this can get.

## What you learned

- Big O describes how the work grows with the input, written with `n`, and it counts steps rather than seconds.
- O(1) is an index, `push` or a `Map` or `Set` lookup; O(log n) halves the problem each step; O(n) touches every item once; O(n log n) is sorting; O(n²) is a loop in a loop.
- Drop the constants, keep the biggest part, and count the worst case.
- `includes`, `indexOf`, `find`, `slice`, spread and `shift` each hide a loop, so using one inside a loop is quadratic.
- A `Set` instead of `includes` inside a loop is the most common fix.

## Common questions

**What is Big O notation in JavaScript?** It is a short way to describe how the number of steps your code takes grows as the input grows. O(n) means the work grows in step with the number of items; O(n²) means it grows with the square.

**Is `includes` O(n) in JavaScript?** Yes. It walks the array from the start until it finds the value, so in the worst case it checks every item. `Set.prototype.has` is O(1) on average.

**Why is a loop with `includes` inside it slow?** The loop runs n times and each `includes` walks up to n items, so the total is n times n. In the test above, 40,000 items took about 883 ms with an array and under 5 ms with a `Set`.

**Is `shift` slower than `pop`?** `pop` removes the last item and is O(1). `shift` removes the first item, so every other item moves one place, which is O(n). Use a head pointer or a proper queue for large queues.

**Should I always use the lowest Big O?** No. Big O describes growth, so on small lists a simpler approach can be as fast or faster. Measure first, then fix the one slow part.

Next lesson: closures and scope, how a function can remember the variables around it.
