title: JavaScript objects: keys, methods, spread and more
summary: How you group related values under names: object literals, the dot and brackets, methods and this, destructuring, spread, optional chaining, Object.keys, values and entries, and why a copy is not a second name. Three short programs with their real output.
description: JavaScript objects for beginners: keys and values, dot vs brackets, methods and this, destructuring, spread, optional chaining and Object.entries, with real output.
date: 2026-11-14
read: 8 min read
lesson: 10
video: Objects | https://youtu.be/1kgde3om_H8
image: cover.png
---
This lesson is about JavaScript objects: how you keep related values together under names. By the end of this page you will write an object, read and change what is inside it with the dot and with brackets, give an object a method that uses `this`, pull values out with destructuring, copy and merge objects with spread, stop a missing value from crashing your program with `?.`, and loop over an object with `Object.keys`, `Object.values` and `Object.entries`.

## Why objects, not arrays

An array finds each item by its position: number zero, number one, number two. That is perfect for many things of the same kind, like prices. But a user has a name, an age and a city, which are different details of one thing. In an array you would have to remember that place zero is the name and place one is the age. An object lets you use the names themselves. Each name is a key, what it holds is the value, and a key with its value is a property.

## Write an object with curly braces

Picture a cabinet of drawers, each with a label. Here is the first program. It builds a `user`, reads from it, changes it and prints it.

```js
const user = {
  name: "Maya",
  age: 29,
  city: "Pune",
  greet() {
    return `Hi, I'm ${this.name}`;
  },
};
console.log(user.name);
console.log(user["age"]);
const key = "city";
console.log(user[key]);
user.age = 30;
user.email = "maya@example.com";
delete user.city;
console.log(user.greet());
console.log(user);
```

```output
Maya
29
Pune
Hi, I'm Maya
{
  name: 'Maya',
  age: 30,
  greet: [Function: greet],
  email: 'maya@example.com'
}
```

Keys are usually plain words with no quotes, and values can be anything: text, numbers, booleans, arrays or other objects. After an `=` sign, curly braces mean an object. After an `if` or a function, they mean a block of code.

## Read values: the dot and brackets

`user.name` is the one you will use almost all the time. `user["age"]` does the same with a string in square brackets. Brackets exist because they accept a variable: with `const key = "city"`, `user[key]` looks up the drawer whose label is stored in `key`. `user.key` would look for a drawer literally called `key`. Use the dot when you know the name, and brackets when the name is in a variable or has a space or a dash in it. A key that is not there gives `undefined`, not an error.

## Change, add and delete properties

`user.age = 30` changes a value. The same line with a new key, `user.email = "maya@example.com"`, adds one. `delete user.city` removes one. You might ask how that works when we wrote `const user`. `const` holds the name tag, not the contents: you cannot point `user` at a different object, but you can change what is inside this one, just like an array.

## Methods and this

A function stored in an object is a method. Inside `greet`, the word `this` means the object the method was called on, so `this.name` reads `user.name` and the result is `Hi, I'm Maya`. Write methods in the short form shown above. An arrow function does not get its own `this`, so it is the wrong shape for a method.

## Destructuring, spread and optional chaining

The second program unpacks, merges and reads safely.

```js
const { name, age = 18, city: town = "Unknown" } = { name: "Sam", city: "Goa" };
console.log(name, age, town);

const defaults = { theme: "dark", size: 12 };
const mine = { size: 16 };
const settings = { ...defaults, ...mine };
console.log(settings);

const profile = { name: "Maya", address: { city: "Pune" } };
console.log(profile.address.city);
console.log(profile.contact?.email);
console.log(profile.contact?.email ?? "no email");
```

```output
Sam 18 Goa
{ theme: 'dark', size: 16 }
Pune
undefined
no email
```

Destructuring matches by key name, so the order does not matter. `age = 18` is a default, used because the object has no `age`. `city: town` is a rename: the value of `city` lands in a variable called `town`.

Spread, three dots inside new curly braces, copies every property of an object into the new one. With two objects, the one written last wins: `mine` covers the `size` from `defaults`, so you get `theme` dark and `size` 16.

`profile.contact.email` would throw a TypeError, because `contact` is `undefined` and you cannot read a property of `undefined`. Put a question mark before the dot, `profile.contact?.email`, and the chain stops at the missing value and gives `undefined`. Add `??` for a default. Use `?.` where something can really be missing, not everywhere, or you will hide real bugs.

## Object.keys, Object.values and Object.entries

You do not loop over an object directly. You turn it into an array first. The third program does that, then shows why a copy is not a second name.

```js
const stock = { apples: 4, pears: 0, plums: 7 };
console.log(Object.keys(stock));
console.log(Object.values(stock));
console.log(Object.entries(stock));
for (const [fruit, count] of Object.entries(stock)) {
  console.log(`${fruit}: ${count}`);
}

const copy = { ...stock };
copy.apples = 99;
const same = stock;
same.pears = 5;
console.log(stock.apples, stock.pears, copy.apples);
```

```output
[ 'apples', 'pears', 'plums' ]
[ 4, 0, 7 ]
[ [ 'apples', 4 ], [ 'pears', 0 ], [ 'plums', 7 ] ]
apples: 4
pears: 0
plums: 7
4 5 99
```

`Object.keys` gives the labels, `Object.values` what is inside, and `Object.entries` gives pairs, each a small array with the key first and the value second. Destructuring each pair in a `for...of` gives you the label and the value on every turn.

Objects are passed by reference. `const same = stock` does not copy anything: it gives the same object a second name, so setting `same.pears = 5` changes `stock.pears` too. Spread makes a real copy, so changing `copy.apples` leaves `stock.apples` at 4. The last line prints `4 5 99`.

## Mistakes to avoid

- Using the dot when the key is in a variable. `user.key` looks for a drawer called `key`.
- Thinking `const` freezes an object. It only stops you pointing the name somewhere else.
- Comparing objects with `===`. Two objects with the same contents are still two objects, so you get `false`.
- Reading inside a missing property and getting a TypeError. Use `?.` when it might be missing.
- Copying with `=` and changing the original by accident. Use spread.
- Writing a method as an arrow function, where `this` is not the object.

## What you learned

- An object groups values under keys, and each key with its value is a property.
- Read with the dot, or with brackets when the key is in a variable. A missing key gives `undefined`.
- Assigning to a new key adds a property, and `delete` removes one, even on a `const` object.
- A function inside an object is a method, and `this` is the object it was called on.
- Destructuring pulls values out, with defaults and new names.
- Spread copies and merges objects, and the last one wins.
- `?.` stops a missing value from crashing your program, and `??` gives a default.
- `Object.keys`, `Object.values` and `Object.entries` turn an object into arrays you can loop over.
- `const same = stock` is a second name, not a copy.

## Common questions

**How do I check whether a key exists?** Use `"age" in user` or `Object.hasOwn(user, "age")`. Reading `user.age` and checking for `undefined` can mislead you, because a key can exist and hold `undefined`: with `{ nick: undefined }`, `"nick" in obj` is `true`.

**How do I use a key with a space in it?** Use brackets and a string: `user["first name"]`. The dot only works for names written like variables.

**Is spread a deep copy?** No, it is shallow. If a property holds another object, the copy and the original share that inner object. With `const a = { n: { x: 1 } }` and `const b = { ...a }`, setting `b.n.x = 9` also changes `a.n.x`. For a full deep copy, use `structuredClone(a)`.

**Why is `{} === {}` false?** Each pair of curly braces makes a new object, and `===` asks whether two names point at the very same object. To compare contents, compare the properties one by one.

**Does the order of keys matter?** Keys come out in the order they were added, except whole-number keys, which come first in number order: `Object.keys({ b: 1, a: 2, 1: "x" })` gives `[ '1', 'b', 'a' ]`. If order matters a lot, a `Map` is the better tool.

Next in the series: maps and sets, two more ways to keep collections when a plain object is not the best fit.
