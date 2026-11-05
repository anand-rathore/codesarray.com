title: JavaScript conditionals: if else, switch, === and ??
summary: How your code makes decisions: why to always use triple equals, which values are truthy and falsy, if, else if and else, switch with break, the ternary, and, or, short circuiting, and the nullish operator for defaults. Two short programs with their real output.
description: JavaScript conditionals for beginners: always use ===, truthy and falsy values, if else if else, switch and break, the ternary, && and ||, and ?? for defaults.
date: 2026-11-05
read: 9 min read
lesson: 5
video: Conditionals and Logic | https://youtu.be/fkQISHOci7w
image: cover.png
---
This lesson is about JavaScript conditionals: how your code makes decisions. By the end of this page you will compare values the safe way and know why you should always use triple equals, you will know which values count as true and which as false, you will write `if`, `else if` and `else`, a `switch` and a one line ternary, and you will use `&&`, `||` and the nullish operator `??` to pick defaults.

## Asking a question: === and ==

Every decision starts with a question, and the answer is always `true` or `false`: a boolean. The simplest question is "are these two things the same?". Picture a bouncer at a door checking a name against the guest list. In JavaScript the bouncer is `===`, triple equals.

`3 === 3` is `true`. `3 === "3"` is `false`. Triple equals is strict: it checks the value and the type, so a number is never the same as text.

There is also `==`, double equals, the loose one. Before it compares, it quietly converts the values to match, so `3 == "3"` is `true`. That sounds helpful, but it leads to strange answers: `0 == ""` is `true`, `null == 0` is `false`, and `null == undefined` is `true`. Nobody remembers all the rules, so the rule is simple: always use `===`. Its opposite is `!==`, "not the same". The others you already know: `>`, `<`, `>=` and `<=`. All of these give you a boolean.

## Truthy and falsy

An `if` does not need a real `true` or `false`. It accepts any value, and JavaScript quietly asks: is this value truthy or falsy? Think of a light switch: every value is either on or off.

Only six values are off. They are called falsy:

- `false`
- `0`
- `""` (an empty string)
- `null`
- `undefined`
- `NaN`

Everything else is truthy. That includes `-1`, the string `"0"`, the string `"false"`, and, surprisingly, an empty list `[]` and an empty object `{}`: they are on because they exist. You can check any value with `Boolean`: `Boolean("")` is `false`, `Boolean("0")` is `true`, `Boolean([])` is `true`.

This is handy: `if (name)` is false when the box is empty. Be careful with numbers, though, because `0` is falsy, so `if (cups)` treats zero cups as nothing at all. We come back to that below.

## if, else if and else

Picture a fork in the road. Write `if`, the question in round brackets, then curly braces with the code to run. If the question is truthy the code runs, and if not JavaScript skips it. Add `else` for the road for everything else, and as many `else if` in between as you like.

JavaScript goes down the list from the top, and the first one that is true wins. The rest are skipped. With a temperature of 31, `temp > 30` is true, so it prints `iced drink` and never looks at the other two. That means the order matters: put the biggest check first. If you put `temp > 15` first, 31 would match it and you would never see `iced drink`. Always use the curly braces, even for one line, so the code stays safe when you add a second line later.

## switch

When you check one value against a list of exact choices, there is a tidier tool: `switch`. Picture the menu board at a cafe: small, medium, large. Write `switch (size)`, then a `case` for each choice with a colon and the code to run.

After each case, write `break`. Without it JavaScript does not stop: it falls through and runs the next case as well. At the bottom, add a `default`, which is the `else` of a switch and runs when nothing matched. A switch matches strictly, like `===`, so the string `"3"` will not match the number `3`. Use `if` for questions like "greater than", and `switch` for one value with many exact choices.

## The ternary

For a tiny decision there is the ternary: a quick yes or no question in one line. The question, then `?`, then the value if true, then `:`, then the value if false. `cups > 1 ? "cups" : "cup"` gives `"cups"` for three cups and `"cup"` for one.

The big difference from `if` is that a ternary gives you back a value, so you can save it in a `const` or drop it inside a sentence. Use it for small, simple choices. If you catch yourself putting one ternary inside another, write an `if` instead.

## And, or and not

To ask two questions at once, use `&&` (and), `||` (or) and `!` (not). Picture a door with two locks. `&&` needs both to be true: both locks open. `||` needs only one: either key works. `!` flips a boolean, so `!true` is `false`.

These two have a trick: they do not just give back `true` or `false`, they give back one of the actual values.

- `||` looks at the left side. If it is truthy, you get the left side and the right is never looked at. If it is falsy, you get the right side. So `typed || "guest"` is `"guest"` when `typed` is an empty string. That is the classic way to write a default.
- `&&` does the opposite. If the left side is falsy you get the left side and it stops. If it is truthy, you get the right side. It is a guard: `order && order.cups` gives `null` when `order` is `null`, and `order.cups` never runs.

Stopping as soon as the answer is known is called short circuiting.

## The nullish operator

There is a problem with `||`: zero is falsy. Say `cups` is `0` and you write `cups || 1` as a default. You get `1`, but `0` was a real answer: the customer wanted zero cups.

The nullish operator `??` fixes this. It replaces only two values, `null` and `undefined`. Zero stays zero, an empty string stays an empty string, and `false` stays `false`. So `cups ?? 1` is `0`, while `null ?? "none"` and `undefined ?? "none"` are both `"none"`. The rule: use `||` when any empty value should get a default, and `??` when only a missing value should.

## The cafe program

```javascript
// a cafe decides what to do
const temp = 31;
if (temp > 30) {
  console.log("iced drink");
} else if (temp > 15) {
  console.log("flat white");
} else {
  console.log("hot chocolate");
}

const size = "large";
switch (size) {
  case "small":
    console.log("200 ml");
    break;
  case "large":
    console.log("400 ml");
    break;
  default:
    console.log("ask the customer");
}

const cups = 3;
console.log(cups === 3, cups === "3");
const label = cups > 1 ? "cups" : "cup";
console.log(`${cups} ${label}`);
```

```output
iced drink
400 ml
true false
3 cups
```

Lines 3 to 9 are the fork in the road: line 3 asks if it is over 30, line 5 is the `else if`, and line 7 is the `else`. Line 12 opens the `switch`, and with the size `"large"` it jumps to the `case "large"` on line 16, prints `400 ml`, and the `break` on line 18 stops it falling through. Line 24 compares `cups` with `3` and with the string `"3"` using triple equals, line 25 is the ternary that picks `cups` or `cup`, and line 26 drops that label into a sentence.

## The truthy, falsy and defaults program

```javascript
// truthy, falsy and defaults
console.log(Boolean(""), Boolean("0"), Boolean(0), Boolean([]));
console.log(Boolean(null), Boolean(undefined), Boolean(NaN));

const typed = "";
const name = typed || "guest";
console.log(name);

const cups = 0;
console.log(cups || 1, cups ?? 1);

const order = null;
console.log(order && order.cups);
console.log(null ?? "none", undefined ?? "none");
```

```output
false true false true
false false false
guest
1 0
null
none none
```

Line 2 checks four values with `Boolean`: the empty string is off, the string `"0"` is on, the number `0` is off, and the empty list is on. Line 3 shows that `null`, `undefined` and `NaN` are all off. Line 6 uses `||` to fall back to `"guest"`. Line 10 prints `cups || 1` next to `cups ?? 1`: `||` threw away the real zero and `??` kept it. Line 13 uses `&&` as a guard, so `order.cups` never runs, and line 14 shows `??` giving `"none"` for both missing values.

## What you learned

- `===` checks the value and the type, so always use it. `==` converts first and gives odd answers.
- Six values are falsy: `false`, `0`, `""`, `null`, `undefined` and `NaN`. Everything else is truthy.
- `if`, `else if` and `else` go down the list, and the first true branch wins.
- `switch` matches one value against exact cases, and each case needs a `break`.
- The ternary picks one of two values in a line, and it gives back a value.
- `&&`, `||` and `!` combine questions, `||` gives a default, and `&&` can guard.
- `??` only replaces `null` and `undefined`, so a real `0` survives.

## Common questions

**Why should I always use `===` instead of `==`?** Because `==` converts the values before comparing and gives answers that are hard to predict, like `0 == ""` being `true`. `===` checks the value and the type, so it never surprises you.

**Which values are falsy in JavaScript?** `false`, `0`, `""`, `null`, `undefined` and `NaN`. Everything else is truthy, including `"0"`, an empty list `[]` and an empty object `{}`.

**Why does my `switch` run more than one case?** You forgot `break`. Without it, JavaScript falls through and runs the next case as well. End each case with `break`, and add a `default` for everything else.

**What is the difference between `||` and `??`?** `||` replaces any falsy value, so a real `0` or an empty string is lost. `??` replaces only `null` and `undefined`. Use `??` when zero or an empty string is a real answer.

**When should I use a ternary instead of an if?** For a small choice between two values, like `cups > 1 ? "cups" : "cup"`. For anything bigger, or a ternary inside a ternary, write an `if`.

Next in the series: loops.
