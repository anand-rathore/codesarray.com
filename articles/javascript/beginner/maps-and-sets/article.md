title: JavaScript Map and Set: keys, values, unique items and union
summary: How you store key and value pairs in a Map and unique values in a Set: set, get, has, delete, looping in order, Map or object, removing duplicates, union, intersection and difference, and counting words. Three short programs with their real output.
description: JavaScript Map and Set for beginners: set, get, has, Map vs object, remove duplicates, union, intersection and difference, with real output.
date: 2026-11-16
read: 8 min read
lesson: 11
video: Maps and Sets | https://youtu.be/FwFUIfE0VMo
image: cover.png
---
This lesson is about the JavaScript Map and Set: two built-in collections for jobs a plain object or array does badly. By the end of this page you will store key and value pairs in a Map and read, check and delete them, know when a Map is a better choice than an object, remove duplicates with a Set, check membership quickly, loop over both in the order you added things, and combine two sets with `union`, `intersection` and `difference`.

## Why Map and Set

Objects are great for one thing with known names, like a user. But the keys of an object are always text, so a number you put in quietly becomes a string. An object also comes with some keys of its own, and it has no simple way to tell you how many things it holds. And asking an array "is this in here?" with `includes` means looking at the items one by one. A Map is for key and value pairs. A Set is for a collection of unique values. Both remember the order you added things in.

## Map: set, get, has, delete and size

Picture a coat check. You hand over a coat and get a ticket, and the ticket gets the same coat back. A Map works the same way: `set` puts a value in under a key, `get` reads it back, `has` asks if a key is there, `delete` removes one, and `size` says how many pairs are inside. Note that `size` is a property, so it has no brackets. A key that is not there gives `undefined`, just like an object.

## Map keys can be anything

A Map key can be a number, an object, even a function, and it stays exactly what you gave it. In the last two lines of the first program, the number `1` finds `"one"`, but the text `"1"` finds nothing, because they are two different keys. In a plain object both would be the same key, since every object key becomes text. A Map also has no hidden keys of its own, so it is safe for names you do not control, like words typed by users.

## Loop over a Map

You can loop straight over a Map with `for...of`. Each time round you get a pair, a small array with the key first and the value second, so you destructure it right in the loop. No `Object.entries` is needed. The order is the order you added things in: apples first, then plums, since pears was deleted. A Map also has `keys()`, `values()` and `entries()` built in.

```js
const stock = new Map();
stock.set("apples", 4);
stock.set("pears", 0);
stock.set("plums", 7);
console.log(stock.get("apples"));
console.log(stock.has("kiwi"));
console.log(stock.size);
stock.delete("pears");
for (const [fruit, count] of stock) {
  console.log(`${fruit}: ${count}`);
}
const ids = new Map([[1, "one"], [2, "two"]]);
console.log(ids.get(1), ids.get("1"));
```

```output
4
false
3
apples: 4
plums: 7
one undefined
```

Lines 2 to 4 put in three fruits. Line 5 reads the apples and line 6 asks about a kiwi. Line 7 prints the size, which is `3` because the delete in line 8 has not run yet. Lines 9 to 11 loop over what is left, so only apples and plums print. Line 12 makes a Map from pairs, and line 13 reads key `1` and then the text `"1"`.

## Map or plain object

Use a plain object when you describe one thing with a fixed set of names that you know when you write the code, like a user with a name, an age and a city. Use a Map when it is a lookup table: keys you add and remove while the program runs, keys that are not always text, or when you need the size quickly. Counting words, caching results and linking an id to a record are Map jobs. One thing to remember: a Map does not turn into JSON by itself. `JSON.stringify` of a Map gives `{}`, so turn it into an array of entries first, with `[...map]`.

## Set: remove duplicates

A Set is a collection where every value can appear only once. Give `new Set` an array and it takes in every item, ignoring the repeats, like a guest who signs in twice but is only counted once. A list of tags `js`, `node`, `js`, `css`, `node` becomes just three. To get a normal array back, spread the Set: `[...unique]`. That is the shortest way in JavaScript to remove duplicates from an array.

## Set: add, has and delete

`add` puts a value in, and adding something that is already there changes nothing. `has` asks if a value is there, and `delete` removes one. A Set finds a value almost instantly however big it is, while an array with `includes` has to look at the items one by one. For ten items you will never notice, and for a hundred thousand you will.

## Union, intersection and difference

These three arrived in ES2025, and Node 24 has them. Think of two guest lists side by side. `a.union(b)` gives everyone on either list, `a.intersection(b)` gives only the people on both, and `a.difference(b)` gives the people on `a` who are not on `b`. Each one returns a brand new Set and leaves `a` and `b` as they were.

```js
const tags = ["js", "node", "js", "css", "node"];
const unique = new Set(tags);
console.log(unique);
console.log([...unique]);
unique.add("html");
unique.add("js");
console.log(unique.size);
console.log(unique.has("css"));
unique.delete("css");

const a = new Set([1, 2, 3]);
const b = new Set([3, 4]);
console.log(a.union(b));
console.log(a.intersection(b));
console.log(a.difference(b));
```

```output
Set(3) { 'js', 'node', 'css' }
[ 'js', 'node', 'css' ]
4
true
Set(4) { 1, 2, 3, 4 }
Set(1) { 3 }
Set(2) { 1, 2 }
```

Line 2 makes a Set from the repeated list. Line 4 spreads it into an array. Lines 5 and 6 add `"html"` and a second `"js"`, so the size in line 7 is `4`, not `5`. Line 8 asks about `"css"` and line 9 deletes it. Lines 13 to 15 print the three combinations.

## getOrInsert, coming in ES2026

Counting needs the same three steps every time: get the value, check if it is there, and set a starting value if not. The ES2026 method `getOrInsert` does that in one step: `stock.getOrInsert(key, 0)` gives you the value if the key is there, or puts in `0` and gives you `0`. It is not in Node 24 yet, so it is not in the programs here. Until it ships everywhere, the pattern `counts.get(word) ?? 0` works the same way.

## Count words and spot repeats

The third program counts how often each word appears with a Map, then uses a Set to find the repeats. In the loop, `counts.get(word) ?? 0` gives the current count or zero for a new word, and adding one and setting it back keeps the tally. For the repeats, a word that is already in `seen` goes into `dupes`, and then it is added to `seen`. The first `"ant"` is not listed as a repeat because at that point it was new.

```js
const words = ["ant", "bee", "ant", "cat", "bee", "ant"];
const counts = new Map();
for (const word of words) {
  counts.set(word, (counts.get(word) ?? 0) + 1);
}
console.log(counts);
console.log([...counts.keys()]);
console.log([...counts.values()]);
console.log([...counts.entries()]);

const seen = new Set();
const dupes = [];
for (const word of words) {
  if (seen.has(word)) dupes.push(word);
  seen.add(word);
}
console.log(dupes);
```

```output
Map(3) { 'ant' => 3, 'bee' => 2, 'cat' => 1 }
[ 'ant', 'bee', 'cat' ]
[ 3, 2, 1 ]
[ [ 'ant', 3 ], [ 'bee', 2 ], [ 'cat', 1 ] ]
[ 'ant', 'bee', 'ant' ]
```

## Mistakes to avoid

- Using square brackets on a Map. `stock["apples"] = 4` does not use the Map at all, it adds a plain property to the object. Always use `set` and `get`.
- Writing `stock.size()` or `stock.length`. A Map and a Set have `size`, with no brackets, and no `length`.
- Expecting two equal objects to match. A Set holds two objects with the same contents as two separate items, because each is a different object.
- Expecting a Set to have positions. There is no "set at zero". Spread it into an array first.
- Printing a Map with `JSON.stringify` and getting `{}`. Turn it into an array of entries first.

## What you learned

- A Map holds key and value pairs, and its keys can be any type.
- Use `set`, `get`, `has`, `delete` and `size`, and loop with `for...of` in the order things were added.
- Pick a Map for lookups that change, and an object for one thing with known names.
- A Set holds each value once, and `[...new Set(list)]` removes duplicates.
- `union`, `intersection` and `difference` combine sets and return a new Set.
- `getOrInsert` is coming in ES2026, and `?? 0` does the same job today.

## Common questions

**Should I use a Map or a plain object?** Use an object for one thing with a fixed set of names, like a user. Use a Map for a lookup table where keys come and go, are not always text, or where you need `size` straight away.

**Does a Set keep the order I added things in?** Yes. A Set and a Map both remember insertion order, and looping over them gives that order.

**How do I save a Map as JSON?** `JSON.stringify` of a Map gives `{}`. Turn it into an array of pairs with `[...map]`, or into a plain object with `Object.fromEntries(map)`, and stringify that.

**Why does a Set keep two objects that look the same?** A Set compares objects by identity, not by contents, so `{ id: 1 }` twice are two different objects and the size is `2`. Numbers and strings compare by value, and `NaN` counts as equal to itself, so `new Set([NaN, NaN])` has size `1`.

**Are `1` and `"1"` the same key?** Not in a Map or a Set. They are different values, so `new Set([1, "1", 1])` keeps `1` and `"1"`. In a plain object they would be the same key, because every object key becomes text.

Next lesson: errors, what happens when something goes wrong and how to handle it.
