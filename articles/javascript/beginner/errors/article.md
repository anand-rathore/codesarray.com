title: JavaScript error handling: throw, try/catch and custom errors
summary: How you raise an error with throw, recover with try, catch and finally, pick the right built-in error type, write your own error class, keep the original failure with cause, read a stack trace, and check a caught value with ES2026 Error.isError. Three short programs with their real output.
description: JavaScript error handling for beginners: throw, try/catch/finally, custom error classes, cause, stack traces and ES2026 Error.isError, with real output.
date: 2026-11-18
read: 8 min read
lesson: 12
video: Errors | https://youtu.be/hiFLc9EPDbc
image: cover.png
---
This lesson is about JavaScript error handling: what happens when something goes wrong, and how a program survives it. By the end of this page you will raise your own errors with `throw`, catch them with `try` and `catch` so the program recovers instead of crashing, run cleanup with `finally`, know the built-in error types and when to make your own, attach the real reason to an error with `cause`, read a stack trace, and check a caught value with `Error.isError`, new in ES2026.

## What happens when nobody handles an error

An error in JavaScript is like a fire alarm in a building. When something goes wrong, say a function reads a property of `undefined`, JavaScript throws a `TypeError` and the program stops right there. The lines after it never run. In the terminal you get red text: the error's name, its message, and a list of lines showing where it happened. A tiny script can just stop, but a real program should expect trouble and have a plan. JavaScript gives you two tools for that plan: `throw`, to raise the alarm, and `try...catch`, to answer it.

## Throw: raise the alarm yourself

When your own code spots something wrong, you pull the alarm yourself: `throw new Error("cannot divide by zero")`. The moment `throw` runs, the function stops and the error travels up to whoever called it. The Error object carries a `message`, the text you wrote, and a `name`, which is just `Error` for the basic kind. JavaScript will let you throw anything, even a plain string. Don't: a real Error carries its message, its name and the trail of where it happened, while a thrown string carries nothing but itself.

## Try, catch and finally

A `try...catch` is a safety net under a trapeze artist. The risky code goes inside `try`. If nothing goes wrong, the `catch` block is skipped completely. If anything inside `try` throws, the rest of the `try` block is abandoned and the `catch` block runs with the error. Either way, the program carries on after the catch: caught means recovered. The third block, `finally`, runs in every case, after a smooth try or after a catch, so it is the place for cleanup like closing a file or stopping a timer.

```js
function divide(a, b) {
  if (b === 0) {
    throw new Error("cannot divide by zero");
  }
  return a / b;
}

try {
  console.log(divide(10, 2));
  console.log(divide(5, 0));
  console.log("never reached");
} catch (err) {
  console.log("caught:", err.message);
} finally {
  console.log("finally always runs");
}
console.log("program keeps going");
```

```output
5
caught: cannot divide by zero
finally always runs
program keeps going
```

The first divide works and prints `5`. The second throws, so `"never reached"` never prints; the catch receives the error and prints its message. The finally block runs either way, and the last line proves the program is still alive.

## The built-in error types

JavaScript has a small family of error types, like the warning lights on a car dashboard: each one names its own kind of trouble. `TypeError` means a value was the wrong kind of thing, like reading a property of `undefined`. `RangeError` means the value was the right kind but out of bounds. `ReferenceError` means you used a name that does not exist, usually a typo. `SyntaxError` means the code itself could not be read; `JSON.parse` throws it for broken JSON. The name matters because it tells you where to look, and your own code can throw them too: `throw new RangeError(...)` when a number is out of bounds.

## Your own error class

Sometimes you want your own label: not a wrong type, but a wrong age or an unpaid order. The whole recipe is three lines: a class that extends `Error`, a constructor that passes the message up with `super`, and a `name`. Now a catch block can tell your errors apart with `instanceof`, handle yours, and rethrow the rest.

```js
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

function parseAge(text) {
  const age = Number(text);
  if (text.trim() === "" || Number.isNaN(age)) {
    throw new ValidationError(`"${text}" is not a number`);
  }
  if (age < 0 || age > 130) {
    throw new RangeError(`age ${age} is out of range`);
  }
  return age;
}

for (const input of ["42", "abc", "200"]) {
  try {
    console.log("age:", parseAge(input));
  } catch (err) {
    console.log(`${err.name}: ${err.message}`);
  }
}
```

```output
age: 42
ValidationError: "abc" is not a number
RangeError: age 200 is out of range
```

`"42"` passes cleanly. `"abc"` is not a number, so our own `ValidationError` does its job. `200` is a number but out of range, so the built-in `RangeError` fires. Each input goes through its own try/catch, so one bad input never stops the next one.

## Keep the original error with cause

Deep inside a program, something low-level fails: `JSON.parse` chokes on a broken file with a precise but cryptic message. You want to throw a clearer error without losing the original. That is what `cause` is for: `throw new Error("config file is broken", { cause: err })`. It is a returned parcel with a note inside saying exactly why it came back. Whoever catches it reads `err.message` for the clear part and `err.cause` for the original. Two layers, nothing lost.

## Read the stack trace

When an error goes uncaught, JavaScript prints the error and then a list of lines, each starting with `at`. That list is a trail of breadcrumbs from the exact spot the error happened back to where the program started. The top line is where the error was thrown, as file, colon, line number, colon, column. The line below it is the function that called that one, and so on down the chain. Read the message first, then the top line of the trail. If the top lines are inside Node or a library, keep reading down until you hit a file that is yours: that is where you start looking. Every error carries this trail in its `stack` property, even when you catch it.

## Error.isError, new in ES2026

ES2026 adds `Error.isError`, and Node 24 has it. It answers one question: is this thing a real Error object, true or false? You need it because of code that throws strings: if someone threw a plain string, there is no `message` to read. We used to use `instanceof Error`, and it usually works, but values that cross from another window or worker can fail that test even when they are real errors. `Error.isError` gets those right too.

```js
function loadConfig(text) {
  try {
    return JSON.parse(text);
  } catch (err) {
    throw new Error("config file is broken", { cause: err });
  }
}

try {
  loadConfig("{ bad json }");
} catch (err) {
  console.log(err.message);
  console.log("cause:", err.cause.message);
  console.log(Error.isError(err));
  console.log(Error.isError("just a string"));
}
```

```output
config file is broken
cause: Expected property name or '}' in JSON at position 2 (line 1 column 3)
true
false
```

The first line is the message you would show a user, and the cause is the cryptic original you would debug with. Then `true`: the caught error is a real Error. And `false`: a string is just a string, whatever someone threw.

## Mistakes to avoid

- The empty catch block. `catch (err) {}` makes the error vanish and the program limps on with no clue why. At the very least, log it.
- Throwing strings. You lose the name and the trail. Always `throw new Error(...)`.
- Catching too early, in a function that cannot fix the problem. If you cannot recover there, let the error travel up to code that can.
- Using errors for normal life. A wrong password is not an exception, it is a Tuesday. Return a value for things you expect; throw for things that should not happen.
- Forgetting that `finally` runs even after a `return`. It really is every case.

## What you learned

- `throw new Error(...)` raises the alarm and stops the function right there.
- `try...catch` is the safety net: risky code in try, recovery in catch, and the program carries on.
- `finally` runs in every case; put cleanup there.
- `TypeError`, `RangeError`, `ReferenceError` and `SyntaxError` tell you what kind of trouble it is.
- Your own class that extends `Error` is three lines and gives trouble your own label.
- `cause` keeps the original error inside the clearer one.
- The stack trace is the breadcrumb trail: message first, then the top line that is yours.
- `Error.isError`, from ES2026, checks you have really got an Error.

## Common questions

**When should I throw and when should I return a value?** Throw for things that should not happen, like a file that must exist being missing. Return a value, like `null` or `false`, for outcomes you expect in normal use, like a user typing a wrong password.

**Does finally really run after a return?** Yes. `try { return 1; } finally { log(); }` logs before the function hands back `1`. That is what makes finally the right place for cleanup.

**Should I wrap everything in try/catch?** No. Catch only where you can actually recover, like one bad input in a loop. Everywhere else, let the error travel up; an error that reaches the top with a clear message and stack trace is easier to fix than one swallowed halfway.

**What is the difference between err.message and err.cause?** `message` is the text of this error, the clear description you threw. `cause` is the original error you wrapped, with its own message and stack, so nothing about the first failure is lost.

**Why use Error.isError instead of instanceof Error?** They agree almost always, but a value that crossed from another window or worker can fail `instanceof` even though it is a real Error. `Error.isError` answers correctly in those cases too, and it needs Node 24 or newer.

Next lesson: files and JSON, reading and writing real files with Node.
