title: JavaScript variables and data types: let, const, typeof, null
summary: The seven kinds of values JavaScript has, how typeof tells them apart, why typeof null says object, and how to convert text to numbers on purpose.
description: JavaScript variables and data types for beginners: let vs const, the seven primitives, typeof and the typeof null bug, Number() and String(), and why "29" + 1 is "291".
date: 2026-11-01
read: 8 min read
lesson: 2
video: Variables and types | https://youtu.be/nTkoFn2f1XI
image: cover.png
---
This lesson is about JavaScript variables and data types: what kinds of values can go in the boxes you made in lesson 1. By the end of this page you will know the seven kinds of values JavaScript has, you will be able to ask any value what it is with `typeof`, and you will turn text into numbers and back on purpose, instead of letting JavaScript guess.

## let, const, and why not var

`let` makes a box you can change later. `const` makes a box that is locked. Think of a name tag at a conference: your name is printed on it, so that is `const`; the table number on your sticker changes when they move you, so that is `let`. The rule is to start with `const` and switch to `let` only when you actually need to change the value.

Older code and old tutorials use a third word, `var`. It is the original way, from 1995, and it has two bad habits. It ignores curly braces: make a `var` inside an `if` block and you can still read it after the block ends, while `let` stays inside the braces. And `var` lets you declare the same name twice without complaint, where `let` makes that an error and saves you from typos. Modern code uses `const` and `let`. If you see `var`, you are reading old code.

## The seven kinds of values

JavaScript has seven basic kinds of values, called primitives. Primitive just means simple: a single value, not a collection. Picture a sign-up form on a website. The name someone typed is a string, text in quotes. Their age is a number. Whether they ticked the subscribe box is a boolean, `true` or `false`.

JavaScript has just one number type: 29, 3.5 and -2 are all `number`, with no separate integer type. Strings can use double or single quotes as long as you close with the one you opened with. Booleans are written in lower case without quotes; put quotes around `true` and it becomes a string.

The next two are the ones beginners mix up. `undefined` means nothing here yet. Make a box and do not fill it, and JavaScript puts `undefined` in for you: the nickname field the person never reached. `null` means empty on purpose: the form asked for a middle name and the person answered "I don't have one". You will almost never type `undefined` yourself; you will type `null` when you want to mean "deliberately empty".

The last two you will meet rarely. A `bigint` is for whole numbers past about nine quadrillion, where the normal number starts rounding: `2 ** 53 + 1` gives the wrong answer, but `9007199254740993n`, written with an `n` on the end, never rounds. A `symbol` is a unique tag that can never be confused with any other value, used deep inside libraries. For now, just know it exists.

## typeof, and the typeof null bug

Put `typeof` in front of any value or variable and JavaScript hands back a string with the kind's name: `typeof 29` is `"number"`, `typeof "Asha"` is `"string"`, `typeof true` is `"boolean"`, and so on through `"undefined"`, `"bigint"` and `"symbol"`.

Then there is the famous one. `typeof null` says `"object"`. This has been a bug since the first version of JavaScript. Inside the engine every value carried a small type tag, the tag for objects was zero, and `null` was stored as all zeros, so asking for its type read zero and answered "object". By the time anyone wanted to fix it, millions of websites depended on the wrong answer, so it stays forever. The fix is on your side: to check for `null`, do not use `typeof`. Compare directly with triple equals, `value === null`, which gives a plain `true` or `false` and is never wrong.

## The sign-up form as code

```javascript
// a sign-up form someone filled in on our site
const name = "Asha";      // string
let age = 29;             // number
let subscribed = true;    // boolean
let nickname;             // undefined: not set yet
let middleName = null;    // null: empty on purpose
const id = 9007199254740993n; // bigint

console.log(typeof name, typeof age, typeof subscribed);
console.log(typeof nickname, typeof middleName);
console.log(typeof id, typeof Symbol("tag"));

age = 30;            // let: allowed
// name = "Ravi";    // const: TypeError
console.log(name, "is now", age);
```

Line 5 is the interesting one: `let nickname` with no equals sign and no value, so JavaScript fills the box with `undefined`. Line 6 sets `middleName` to `null` ourselves. Line 13 changes `age`, which is fine because it was made with `let`. Line 14 is commented out on purpose: remove the slashes and JavaScript stops with `TypeError: Assignment to constant variable.`, because `name` is `const`. Run it with `node types.js`:

```output
string number boolean
undefined object
bigint symbol
Asha is now 30
```

The second line is the bug, right there: `middleName` is `null`, and `typeof` says `object`.

## Convert on purpose: Number() and String()

Every web form, text field and URL hands your program text, even when someone types a number. If a user types 29 into an age box, your program gets the string `"29"`, not the number 29. Add one to it and the plus sign sees a string, and plus with a string means glue them together: `"29" + 1` is `"291"`. That is a real bug people ship.

The fix is to convert on purpose. `Number()` turns text into a number, so `Number("29") + 1` is 30. `String()` goes the other way and turns anything into text. A few things to know about `Number()`: `Number("3.5")` works, an empty string becomes 0, and text that is not a number, like `"abc"`, becomes `NaN`, "not a number", which is JavaScript's way of saying it couldn't do it.

```javascript
// a web form always hands your program a string
const typed = "29";

console.log(typed + 1);           // plus glues strings
console.log(Number(typed) + 1);   // convert first, then add

console.log(Number("3.5"), Number(""), Number("abc"));
console.log(String(42), String(true), String(null));

console.log("5" - 2, "5" * "2");  // these convert for you
console.log(typeof (typed + 1), typeof (Number(typed) + 1));
```

```output
291
30
3.5 0 NaN
42 true null
3 10
string number
```

Line 10 is the warning. JavaScript will also convert for you when you did not ask, which is called coercion: minus, times and divide turn the string `"5"` into the number 5 on their own. Only plus glues. So the same string behaves differently depending on the operator, which is confusing, and it is why the rule is: don't let JavaScript guess. Convert with `Number()` or `String()` and your code says exactly what it means.

## What you learned

- `const` for boxes that don't change, `let` for boxes that do, and never `var`.
- Seven kinds of values: number, string, boolean, undefined, null, bigint and symbol.
- `undefined` means nothing here yet; `null` means empty on purpose.
- `typeof` tells you the kind, except for `null`, where it says `"object"`; compare with `value === null` instead.
- `Number()` turns text into a number; `String()` turns anything into text.
- Plus with a string glues, so convert first.

## Common questions

**Why does typeof null say object, and will it ever be fixed?** The first JavaScript engine stored a type tag with every value; objects had tag zero and `null` was stored as all zeros, so the check read it as an object. A fix was proposed years later and rejected because too many existing sites depended on the old answer. Use `value === null` to check for null.

**Should I use let or const by default?** `const`. It tells the reader, and JavaScript, that the box never changes, and an accidental reassignment becomes an error instead of a silent bug. Reach for `let` only when the value really has to change, like a counter or a running total.

**Can a let variable change its kind?** Yes. `let x = 29; x = "twenty nine";` is allowed, and `typeof x` follows whatever is in the box now. It is allowed, but it makes code hard to follow, so keep one kind of value per box.

**How do I check whether a conversion failed?** `Number("abc")` gives `NaN`, and `NaN` is the one value that is not equal to itself, so `x === NaN` is always false. Use `Number.isNaN(x)` instead, which is `true` only for `NaN`.

**Is var ever needed?** No. Everything `var` can do, `let` and `const` do without the leaking and the silent redeclaration. You only need to recognise it in code written before 2015.

Next in the series: numbers and math.
