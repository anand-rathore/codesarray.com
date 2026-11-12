title: JavaScript array methods: map, filter, reduce, sort and more
summary: How you work on a whole list at once: forEach, map, filter, reduce, find, findIndex, some and every, the sort comparator gotcha, toSorted and toReversed, and chaining. Three short programs with their real output.
description: JavaScript array methods for beginners: forEach, map, filter, reduce, find, some, every, sort, toSorted and chaining, with real output.
date: 2026-11-12
read: 8 min read
lesson: 9
video: Array methods | https://youtu.be/gcvvnyG7Zl0
image: cover.png
---
This lesson is about JavaScript array methods: how you work on a whole list at once. By the end of this page you will loop over an array with `forEach`, build a new array with `map`, keep only some items with `filter`, boil a list down to one value with `reduce`, search with `find`, `some` and `every`, sort numbers the right way, use `toSorted` and `toReversed` without changing the original, and join the steps into one readable chain.

## Why array methods and callbacks

In the last lesson you stored many values in an array. Now you want to do things with all of them. A loop can do that, but loops are long and you manage the counter yourself. Array methods are shorter: you say what to do with each item, and the array does the looping.

Think of a conveyor belt in a factory. Items roll past, and at one station a worker does something to each one. The thing you hand the array is a small function, called a callback, usually an arrow function such as `(p) => p * 2`. The array calls it once for every item and passes the item in as the first argument.

## forEach: do something with every item

`prices.forEach((p) => console.log(p))` runs your function once for every item, in order. The callback can also take the index as a second argument: `(p, i)`. The catch is that `forEach` gives nothing back, so its result is `undefined`. Use it when you want to do something, like print. When you want a new list, use `map`.

## map: build a new array

`map` runs your function on every item and collects the results into a new array. Think of a photocopier that stamps every page: four pages in, four stamped pages out. `prices.map((p) => p * 2)` turns `5, 12, 8, 20` into `10, 24, 16, 40`. The new array is always the same length as the old one, and the original is not touched. Use `map` to change every item into something else.

## filter: keep only some items

`filter` is a bouncer at a door. Your function must answer yes or no, and only the items that get `true` stay. `prices.filter((p) => p > 7)` keeps `12, 8, 20` and drops `5`. The result can be shorter than the original, or even empty if nobody passes, and again the original is left alone.

## reduce: boil a list down to one value

`reduce` is the till in a shop, adding up your bill. Its function takes two arguments: the running total so far, called the accumulator, and the current item. The second argument to `reduce` itself is where the total starts. `prices.reduce((sum, p) => sum + p, 0)` goes `0 + 5 = 5`, `5 + 12 = 17`, `17 + 8 = 25`, `25 + 20 = 45`. Whatever your function returns becomes the running total for the next step. Always give `reduce` a starting value: on an empty array with no starting value it throws a `TypeError`, and with one it simply returns that value.

## find, some and every

`find` gives back the first item that passes your test, and stops looking right there. If nothing passes, you get `undefined`. `findIndex` does the same but gives the position, or `-1` when nothing matches.

`some` asks whether at least one item passes, and `every` asks whether all of them do. Both stop as soon as the answer is clear. One odd fact: `every` on an empty array is `true`, because nobody breaks the rule, and `some` on an empty array is `false`.

## sort and the comparator gotcha

By default, `sort` turns everything into text and sorts it like words in a dictionary. So `[10, 9, 1, 100].sort()` gives `[1, 10, 100, 9]`: as text, `"1"` comes before `"9"`, and `"100"` starts with a `"1"`. Think of house numbers sorted as words. The fix is a comparator, a function that takes two items and returns a number. If it is negative, `a` goes first; if positive, `b` goes first. So `(a, b) => a - b` sorts small to big, and `(a, b) => b - a` sorts big to small. Remember that `sort` changes the original array.

## toSorted and toReversed

`toSorted` does what `sort` does but hands you a new sorted array and leaves the original alone. `toReversed` does the same for `reverse`. They work in current Node and current browsers. The older way is to copy first with spread and then sort the copy: `[...nums].sort((a, b) => a - b)`.

## Chaining array methods

Every method that gives back an array can be followed by another, which is called chaining. Filter the prices over 7, double them, and add them up: `12, 8, 20` becomes `24, 16, 40`, which adds up to `80`. Write each step on its own line, starting with a dot, and it reads like a recipe: keep the ones over seven, double them, add them up.

## Common mistakes

- Using `forEach` and expecting a new list. It gives back `undefined`, so use `map`.
- Forgetting `return`. If your arrow function has curly braces you must write `return`, otherwise every item becomes `undefined`.
- Sorting numbers without a comparator, which gives text order.
- Calling `reduce` with no starting value on a list that might be empty.
- Forgetting that `sort` changes the original. Use `toSorted`, or copy first.

## The code, line by line

The first program uses `forEach`, `map`, `filter` and `reduce`:

```javascript
const prices = [5, 12, 8, 20];
prices.forEach((p) => console.log(p));

const doubled = prices.map((p) => p * 2);
console.log(doubled);

const big = prices.filter((p) => p > 7);
console.log(big);

const total = prices.reduce((sum, p) => sum + p, 0);
console.log(total);
console.log(prices);
```

```output
5
12
8
20
[ 10, 24, 16, 40 ]
[ 12, 8, 20 ]
45
[ 5, 12, 8, 20 ]
```

`forEach` prints each price on its own line. `map` doubles them, `filter` keeps the ones over 7, and `reduce` adds them to `45`. The last line shows `prices` is unchanged.

The second program finds and checks:

```javascript
const ages = [31, 17, 24, 19];
console.log(ages.find((a) => a < 18));
console.log(ages.findIndex((a) => a > 30));
console.log(ages.find((a) => a > 99));

console.log(ages.some((a) => a < 18));
console.log(ages.every((a) => a >= 18));
console.log([].every((a) => a >= 18));
```

```output
17
0
undefined
true
false
true
```

`find` gives `17`, the first age under 18. `findIndex` gives `0`, because `31` is at index 0. Nobody is over 99, so `find` gives `undefined`. `some` is `true`, `every` is `false`, and `every` on an empty list is `true`.

The third program sorts and chains:

```javascript
const nums = [10, 9, 1, 100];
const copy = [...nums];
console.log(copy.sort());
console.log(nums.toSorted((a, b) => a - b));
console.log(nums.toReversed());
console.log(nums);

const prices = [5, 12, 8, 20];
const result = prices
  .filter((p) => p > 7)
  .map((p) => p * 2)
  .reduce((sum, p) => sum + p, 0);
console.log(result);
```

```output
[ 1, 10, 100, 9 ]
[ 1, 9, 10, 100 ]
[ 100, 1, 9, 10 ]
[ 10, 9, 1, 100 ]
80
```

The plain `sort` gives the text order `[ 1, 10, 100, 9 ]`. `toSorted` with `a - b` gives the right order, `toReversed` flips the list, and `nums` itself is unchanged. The chain at the end gives `80`.

## What you learned

- A callback is a small function you hand to an array, and the array calls it once per item.
- `forEach` runs a function on every item and gives back nothing.
- `map` changes every item into a new array of the same length.
- `filter` keeps the items that pass a yes or no test.
- `reduce` boils a list down to one value, so give it a starting value.
- `find` gives the first match, `findIndex` its position, and `some` and `every` answer yes or no.
- `sort` needs a comparator for numbers, and it changes the original.
- `toSorted` and `toReversed` give a new array and leave the original alone.
- Chaining joins the steps into one pipeline.

## Common questions

**Can I stop a `forEach` early?** No. `break` inside a `forEach` callback is a `SyntaxError`, and `return` only skips to the next item. Use a `for...of` loop with `break`, or `find`, `some` or `every`, which stop as soon as the answer is clear.

**What is the difference between `map` and `forEach`?** `map` gives back a new array of the results, and `forEach` gives back `undefined`. If you want a new list, use `map`. If you only want a side effect like printing, use `forEach`.

**Do `map` and `filter` change the original array?** No. Both give back a new array and leave the original as it was. `sort` is the one that changes the original, which is why `toSorted` exists.

**Why did my `map` give a list of `undefined`?** Your arrow function has curly braces but no `return`. With braces you must write `return`, or drop the braces and write the value directly: `(p) => p * 2`.

**How do I sort text?** `["b", "a", "C"].sort()` gives `[ 'C', 'a', 'b' ]`, because capital letters come first. For human order, use a comparator with `localeCompare`: `toSorted((x, y) => x.localeCompare(y))` gives `[ 'a', 'b', 'C' ]`.

Next in the series: objects, where you group related values together under names.
