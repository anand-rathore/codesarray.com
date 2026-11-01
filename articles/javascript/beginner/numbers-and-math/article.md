title: JavaScript numbers and math: 0.1 + 0.2, NaN, rounding, BigInt
summary: Why 0.1 + 0.2 is not quite 0.3 and how to round it, what NaN and Infinity are, the Math toolbox, parseInt for text with units, and BigInt for numbers past nine quadrillion.
description: JavaScript numbers and math for beginners: why 0.1 + 0.2 prints 0.30000000000000004, Math.round and toFixed, NaN and Number.isNaN, parseInt("42px"), and when to use BigInt.
date: 2026-11-01
read: 10 min read
lesson: 3
video: Numbers and math | https://youtu.be/RcyVotTzUNU
image: cover.png
---
This lesson is about JavaScript numbers and math: what the one number type can do, and where it trips people up. By the end of this page you will know why `0.1 + 0.2` is not quite `0.3` and what to do about it, you will round numbers the way a shop does, and you will turn text like `"42px"` into a real number you can do math with.

## One number type

In many languages, whole numbers and decimals are two different types. Not in JavaScript. `3`, `3.5` and `-2` are all just `number`. Think of a cafe till: a coffee is 3, a muffin is 2.5, and the till does not care which one has a decimal point. It adds them the same way, and `3 + 2.5` is `5.5` without you ever saying which kind of number you meant.

Underneath, every number is stored the same way, as a 64-bit floating point value. That is a fancy name for a number that can hold a decimal point, the same format a calculator app uses. You get about 15 to 16 digits of precision, which is plenty for prices, scores and ages. Keep the phrase "floating point" in mind, because it explains the next surprise.

## Why 0.1 + 0.2 is not 0.3

Type `0.1 + 0.2` into the console and JavaScript answers `0.30000000000000004`. Ask whether it equals `0.3` and you get `false`. This is not a JavaScript bug: Python, Java and C give the same answer.

Think about one third of a cup. In decimal that is 0.3333..., and the threes never stop, so you have to cut it off somewhere and what you write down is a tiny bit less than a third. Computers count in binary, in twos rather than tens, and in binary one tenth is one of those numbers that never stops. So `0.1` gets cut off and stored a tiny bit off, the same for `0.2`, and two tiny errors add up to a result just past `0.3`.

The fix is what every shop and bank does. Never compare money with `===`. Round when you show it: `(0.1 + 0.2).toFixed(2)` gives `"0.30"`, with exactly two decimal places. One catch: `toFixed` hands back a string, text that is ready to print, fine for showing but not for more math. Even better, count in cents: 10 + 20 is 30, and whole numbers are always exact, up to a limit we meet at the end.

## NaN and Infinity

Two odd values live inside the number type. `NaN` stands for "not a number", and it is what you get when the math makes no sense. Picture an order form where someone types `hello` into the quantity box and your code multiplies it by the price: `"hello" * 2` is `NaN`, and so is `0 / 0`.

The weird part is that `NaN` is not equal to anything, not even itself. `NaN === NaN` is `false`; it is the only value in JavaScript that does not equal itself, so you cannot check for it with `===`. Use `Number.isNaN(x)` instead, which gives a plain `true` or `false` and is always right. There is also an older global `isNaN` without the `Number.`; it converts first, so it says `true` for the word `"hello"` too. Stick with `Number.isNaN`.

`Infinity` is what you get from dividing by zero. `1 / 0` is `Infinity` and `-1 / 0` is `-Infinity`. Pizza slices per person, with zero people? Infinity slices each. It is a real value: you can compare with it, `Infinity + 1` is still `Infinity`, and any result too big to store becomes `Infinity`. It is rare, but when you see it, a zero got into a division somewhere.

## Rounding: Math.round, floor, ceil and trunc

Ten shared by three friends is `3.3333333333333335`, and nobody pays that. There are four tools, and they round differently. `Math.round` goes to the nearest whole number, so 3.3 becomes 3 and 3.6 becomes 4. `Math.floor` always goes down, to 3. `Math.ceil`, short for ceiling, always goes up, to 4. `Math.trunc` chops off the decimals, which is the same as floor for positive numbers, but for `-3.7` trunc gives `-3` while floor gives `-4`.

Which one you want depends on the story. Ordering pizza for seven people, two slices each, eight slices a box, is 1.75 boxes, and you cannot order a fraction of a box, so `Math.ceil`: two boxes. Showing a price? You want two decimal places, so `(10 / 3).toFixed(2)` gives `"3.33"`, a string. To round to two decimals and keep a number, multiply by 100, round, then divide by 100: `Math.round(share * 100) / 100` is `3.33`.

## The Math toolbox

`Math` is a built-in object, a toolbox of functions and constants ready to use with no import. `Math.max` picks the biggest of a list of numbers and `Math.min` the smallest: give them the week's temperatures and you have the high and the low. `Math.abs` drops the minus sign, so a distance always comes out positive. `Math.sqrt` is the square root. For powers you do not even need Math: `2 ** 10` is `1024`. `Math.PI` is 3.14159..., and `Math.random()` gives a random decimal from 0 up to, but never reaching, 1.

Here is the classic dice roll. `Math.random() * 6` gives 0 to almost 6, `Math.floor` chops that to 0, 1, 2, 3, 4 or 5, and adding 1 gives 1 to 6: `Math.floor(Math.random() * 6) + 1`. You will use it in games and quizzes all the time.

## Number, parseInt and parseFloat

Text is how numbers arrive in real programs: a form field, a width from a style sheet like `"42px"`, a label like `"3.5kg"`. `Number()` is strict. `Number("42")` is `42`, spaces around it are fine, but `Number("42px")` is `NaN` because the whole string has to be a number, and `Number("")` is `0`, which surprises people.

When the text has units on the end, use `parseInt` or `parseFloat`. `parseInt` reads digits from the start and stops at the first thing that is not a digit, so `parseInt("42px")` is `42`. `parseFloat` does the same but keeps the decimal point: `parseFloat("3.5kg")` is `3.5`. They only give up when the text does not start with a number at all; `parseInt("px42")` is `NaN`. The rule: clean input that should be only a number, use `Number()`, and it tells you when something is wrong. Text with units on the end, `parseInt` or `parseFloat`.

## BigInt for numbers past nine quadrillion

JavaScript's number is exact up to about nine quadrillion; `Number.MAX_SAFE_INTEGER` is the exact line, `9007199254740991`. Past it, numbers get rounded because the floating point format is out of digits: `9007199254740992 + 1` gives `9007199254740992` back. Where does that happen in real life? IDs. A post on a big social network has an ID longer than that, and so do some bank transaction numbers. Store one as a number and the last digit quietly changes.

The fix is `bigint`. Write a whole number with an `n` on the end and it is exact no matter how long it gets: `9007199254740992n + 1n` is `9007199254740993n`. The usual operators work as long as both sides are bigints. Mix a bigint with a plain number and JavaScript throws a `TypeError` rather than guess; convert first with `BigInt(10)`. Bigints are whole numbers only. For everyday math stick with number; reach for bigint when you are holding an ID or counting past that line.

## The cafe bill as code

```javascript
// a cafe bill: a 0.10 topping and a 0.20 topping
const toppings = 0.1 + 0.2;
console.log(toppings);
console.log(toppings === 0.3);
console.log(toppings.toFixed(2));
console.log(typeof toppings.toFixed(2));

// 10 shared by 3 friends
const share = 10 / 3;
console.log(share);
console.log(Math.round(share));
console.log(Math.floor(share), Math.ceil(share));
console.log(Math.round(share * 100) / 100);

// the Math toolbox
console.log(Math.max(3, 9, 4), Math.min(3, 9, 4));
console.log(Math.abs(-7), Math.sqrt(16), 2 ** 10);
```

```output
0.30000000000000004
false
0.30
string
3.3333333333333335
3
3 4
3.33
9 3
7 4 1024
```

Line 2 adds two toppings as decimals, and line 3 prints the long `0.3` with the 4 on the end. Line 4 asks if it equals `0.3`: `false`. Line 5 rounds it for display with `toFixed(2)`, and line 6 proves the result is a string. Line 9 divides 10 by 3, and lines 11 and 12 round it three ways. Line 13 is the trick that keeps a number: times 100, round, divide by 100. Lines 16 and 17 try the toolbox.

## Text in, numbers out

```javascript
// numbers that arrive as text, and the odd ones
const typed = "42px";
console.log(Number(typed));
console.log(parseInt(typed));
console.log(parseFloat("3.5kg"));
console.log(Number("  12  "), Number(""));

const bad = Number("abc");
console.log(bad === NaN);
console.log(Number.isNaN(bad));
console.log(1 / 0, -1 / 0);

console.log(Number.MAX_SAFE_INTEGER);
console.log(9007199254740992 + 1);
console.log(9007199254740992n + 1n);
console.log(typeof 10n);
// console.log(10n + 1);  // TypeError: Cannot mix BigInt
```

```output
NaN
42
3.5
12 0
false
true
Infinity -Infinity
9007199254740991
9007199254740992
9007199254740993n
bigint
```

Line 3 tries `Number` on `"42px"` and gets `NaN`, because `Number` is strict; line 4 uses `parseInt`, which reads the digits and stops at the `p`. Line 9 compares a `NaN` with `===`, the wrong way, and line 10 checks it with `Number.isNaN`, the right way. Line 14 goes one past the safe limit with a plain number and the last digit does not move; line 15 does the same sum with bigints and gets the right answer. Line 17 is commented out because mixing a bigint with a plain number is a `TypeError`.

## What you learned

- One number type, stored as 64-bit floating point.
- `0.1 + 0.2` is `0.30000000000000004`, so round money when you show it with `toFixed(2)`, or count in cents.
- `NaN` means the math made no sense; check for it with `Number.isNaN`. `Infinity` comes from dividing by zero.
- `Math.round`, `Math.floor`, `Math.ceil` and `Math.trunc` round four different ways.
- The `Math` toolbox has `max`, `min`, `abs`, `sqrt`, `PI` and `random`.
- `Number()` for clean text, `parseInt` and `parseFloat` when there are units on the end.
- `bigint`, with an `n`, for whole numbers past nine quadrillion.

## Common questions

**Is 0.1 + 0.2 a JavaScript bug?** No. Every language that uses 64-bit floating point gives the same answer, including Python, Java and C. One tenth has no exact binary form, so it is stored a tiny bit off. Round when you display, or work in whole cents.

**Why is NaN not equal to itself?** The floating point standard defines it that way: `NaN` means "no valid number here", and two unknowns are not the same unknown. That is why `x === NaN` is always `false` and why `Number.isNaN(x)` exists.

**When should I use parseInt instead of Number?** When the text has something after the digits, like `"42px"` or `"3 apples"`. `Number` wants the whole string to be a number and gives `NaN` otherwise. For clean input, `Number` is better because that `NaN` tells you something went wrong.

**Does toFixed round correctly for money?** It gives a string with the number of decimals you ask for, rounding to the nearest value, which is fine for showing a price. For adding prices up, keep them in whole cents as numbers and only call `toFixed` on the total you print.

**Can I use bigint for prices or averages?** No. Bigints are whole numbers only, so `5n / 2n` is `2n` and there is no decimal part. Use bigint for IDs and very large counts, and plain numbers for everything else.

Next in the series: strings.
