title: JavaScript functions: declaration, arrow, default, rest and return
summary: How you write steps once and reuse them: function declarations, expressions and arrow functions, parameters and arguments, default values, rest parameters, return, scope, hoisting, and why a function is just a value. Three short programs with their real output.
description: JavaScript functions for beginners: declarations, expressions and arrow functions, parameters, defaults, rest, return, scope, hoisting and callbacks.
date: 2026-11-08
read: 12 min read
lesson: 7
video: Functions | https://youtu.be/TWrc55jbbPA
image: cover.png
---
This lesson is about JavaScript functions: how you write steps once and use them as often as you like. By the end of this page you will write a function three ways (a declaration, an expression and an arrow function), hand it ingredients with parameters, give a spare one with a default value, take any number with a rest parameter, and get a result back with `return`. You will also know what a function can see (scope), why some functions work before you define them (hoisting), and why a function is just a value you can pass around.

## Why functions

Think of a recipe card on the fridge. You write the steps once, give the card a name, and any time you are hungry you say its name. That is a function.

Say you want to greet three people. You could write the same `console.log` three times, but when the greeting changes you would fix it in three places and probably miss one. A function lets you write the steps once. It has a name, a list of ingredients it needs, a body with the steps, and it can hand a result back. Writing the steps is called defining the function, and using them is called calling it. Nothing happens until you call: a recipe card on the fridge does not cook anything by itself.

## Function declaration

The first way is a function declaration. Write `function`, a name, the ingredients in round brackets, then the steps in curly braces:

```javascript
function greet(name) {
  return "Hello, " + name;
}
```

Inside, `return` hands back the text. To call it, write the name and put the real value in round brackets: `greet("Ada")` gives `"Hello, Ada"`, and `greet("Grace")` gives `"Hello, Grace"`. Same card, different ingredient. Careful: `greet` on its own, without brackets, does not run anything. It just points at the function. The brackets are what run it.

## Function expression

The second way is a function expression. The function has no name of its own: you write it on the right side of an equals sign and store it in a variable.

```javascript
const shout = function (name) {
  return name.toUpperCase() + "!";
};
```

You call it the same way: `shout("ada")` gives `"ADA!"`. This works because a function is a value, like a number or a string, and a variable can hold it. Use `const`, so nobody can swap the function for another one by accident. Both ways behave the same when you call them. The differences are how you write them and when they become available, which we get to under hoisting.

## Arrow functions

The third way is the arrow function, and it is what you will see most in modern code. Drop the word `function`, write the ingredient, then an arrow (`=>`), then the result:

```javascript
const double = (n) => n * 2;
```

When the body is a single expression there are no curly braces and no `return`: the result is handed back for you, which is called an implicit return. `double(21)` gives `42`. With more than one parameter, put brackets around them: `(a, b) => a + b`. With none, write empty brackets.

Two traps. If you add curly braces you are back to a normal body, and then you must write `return` yourself, or you get `undefined`. And to return an object straight away, wrap it in round brackets, `() => ({ a: 1 })`, so JavaScript does not think the curly brace starts a body.

## Parameters and arguments

The names in the definition are called **parameters**. The real values you pass when you call are called **arguments**. In `greet(name)`, `name` is the parameter. In `greet("Ada")`, `"Ada"` is the argument.

They are matched by position: the first argument goes into the first parameter, the second into the second. So order matters. With `function subtract(a, b) { return a - b; }`, `subtract(10, 3)` is `7` but `subtract(3, 10)` is `-7`.

JavaScript is relaxed about the count. If you pass too few arguments, the missing parameters are `undefined`, so `subtract(10)` gives `NaN`. If you pass too many, the extras are ignored. There is no error either way. That is friendly, but it can hide mistakes, so check that you pass what the function needs.

## Default values

What if someone forgets an ingredient? Give the parameter a default by writing an equals sign and a value in the parameter list:

```javascript
function price(amount, tax = 0.1) {
  return amount + amount * tax;
}
```

`price(100)` uses the default and gives `110`. `price(100, 0.2)` uses your value and gives `120`. Here is the detail that surprises people: a default only applies when the value is `undefined`, meaning nothing was passed. `null` and `0` count as real values, so the default is ignored. `price(100, 0)` stays `100`, which is exactly what you want.

## Rest parameters

Sometimes you do not know how many values will come, like a basket at the market that takes any number of items. Put three dots before the last parameter:

```javascript
function total(...nums) {
  let sum = 0;
  for (const n of nums) sum += n;
  return sum;
}
```

Every extra argument is collected into a real array called `nums`. `total(1, 2, 3)` makes `nums` the list `[1, 2, 3]`, and you can loop over it with `for...of`, as in the loops lesson. `total()` makes `nums` an empty array, so the loop runs zero times and you get `0`. The rest parameter must be the last one, and a function can only have one.

## return

`return` does two things: it hands a value back to whoever called, and it ends the function right there. Any line after a `return` never runs. That lets you return early, for example when the input is bad, and skip the rest.

A function with no `return` hands back `undefined`. Write an empty function, print the result of calling it, and you see `undefined`. This is the most common function mistake: you do all the work, forget the word `return`, and out comes `undefined`. Also, `console.log` is not the same as `return`. `console.log` shows a value to a human. `return` gives it to your code.

## Scope

Think of each kitchen as having its own private notebook. A variable made inside a function lives only inside that function, and outside nobody can see it.

Say the label outside is `"outer"`. Inside a function we make a new `label` called `"inner"`. They have the same name, but they are two different variables, and the function sees its own first. Call the function and you get `"inner"`. Look outside and the label is still `"outer"`.

A function can also look outward: if it cannot find a name in its own notebook, it checks the kitchen around it. But the outside can never look in. That is a good thing, because every function can use whatever names it likes without bumping into the others.

## Hoisting

Imagine a book whose table of contents is read before you open page one. Before your code runs, JavaScript scans it and registers every function declaration. So you can call a declared function above the line where you wrote it:

```javascript
console.log(hello());
function hello() {
  return "hoisted";
}
```

This works and prints `hoisted`. A function expression or an arrow function is different. Its name is a `const`, and a `const` is not ready until its line runs. Call it early and you get `ReferenceError: Cannot access 'lateArrow' before initialization`. So declarations work from anywhere in the file, while expressions and arrows work only after the line that creates them. To keep code easy to read, define your functions first and use them after.

## Functions as values

Here is the big idea of this lesson: in JavaScript a function is a value. You can store it in a variable, put it in a list, and pass it to another function. It is like handing the recipe card itself to a friend and saying "do this one twice".

```javascript
function twice(fn, value) {
  return fn(fn(value));
}
console.log(twice((n) => n + 3, 10));
```

`twice` takes a function `fn` and a value, runs `fn` on the value, then runs `fn` again on that result. With an arrow that adds 3 and the value `10`, ten becomes thirteen and then sixteen. Notice there are no brackets after the name when you pass a function in: you are giving the card, not cooking. A function passed in like this is called a **callback**, and you will use callbacks all the time in the array methods lesson. And `typeof` a function says `"function"`.

## Five common function mistakes

1. **Forgetting `return`.** You get `undefined`.
2. **Forgetting the brackets when you call.** You get the function itself, not its result.
3. **An arrow with curly braces and no `return`.** Same `undefined` again.
4. **Calling an arrow or a function expression before it is defined.** That is the `ReferenceError`.
5. **Mixing up the order of the arguments.** JavaScript matches by position, so it will not warn you.

## The three ways program

```javascript
// three ways to write a function
function greet(name) {
  return "Hello, " + name;
}

const shout = function (name) {
  return name.toUpperCase() + "!";
};

const double = (n) => n * 2;

console.log(greet("Ada"));
console.log(shout("ada"));
console.log(double(21));
```

```output
Hello, Ada
ADA!
42
```

Lines 2 to 4 are the declaration: `greet` takes `name` and returns `"Hello, "` plus the name. Line 6 starts the function expression stored in `shout`, and line 7 returns the name in capitals with an exclamation mark. Line 10 is the arrow function: `double` returns `n * 2` with no braces. Lines 12 to 14 call the three functions with `"Ada"`, `"ada"` and `21`.

## The defaults, rest and return program

```javascript
// defaults, rest and return
function price(amount, tax = 0.1) {
  return amount + amount * tax;
}
console.log(price(100));
console.log(price(100, 0.2));

function total(...nums) {
  let sum = 0;
  for (const n of nums) sum += n;
  return sum;
}
console.log(total(1, 2, 3));
console.log(total());

function nothing() {}
console.log(nothing());
```

```output
110
120
6
0
undefined
```

Line 2 defines `price` with a default `tax` of `0.1`, and line 3 returns the amount plus the tax. Line 5 passes only `100`, so the default is used. Line 6 passes `0.2`, which replaces it. Line 8 is `total` with a rest parameter, so every argument lands in `nums`. Line 9 starts the sum at `0`, line 10 adds each number, and line 11 returns it. Line 13 sums `1, 2, 3` and line 14 calls it with nothing, so the loop never runs and the answer is `0`. Line 16 is a function with an empty body, and line 17 prints what it gives back: `undefined`.

## The scope and functions as values program

```javascript
// scope and functions as values
const label = "outer";
function show() {
  const label = "inner";
  return label;
}
console.log(show(), label);

function twice(fn, value) {
  return fn(fn(value));
}
console.log(twice((n) => n + 3, 10));
console.log(typeof twice);
```

```output
inner outer
16
function
```

Line 2 sets `label` to `"outer"`. Inside `show`, line 4 makes a new `label` called `"inner"` and line 5 returns it. Line 7 prints the result of `show()` and the outer `label`: `inner outer`. Line 9 is `twice`, which takes a function and a value, and line 10 runs the function and then runs it again on its own result. Line 12 passes an arrow that adds 3 and the value `10`, which gives `16`. Line 13 prints the type of `twice`: `function`.

## What you learned

- A function is a named recipe: define it once, call it with brackets.
- A declaration is hoisted. An expression or an arrow function is not.
- Parameters are names, arguments are values, and a default fills in what is `undefined`.
- A rest parameter collects the extra arguments into an array.
- `return` hands a value back, and without it you get `undefined`.
- Variables inside a function stay inside.
- A function is a value, so you can pass one to another function as a callback.

## Common questions

**What is the difference between a function declaration and a function expression in JavaScript?** A declaration (`function greet() {}`) has its own name and is hoisted, so you can call it before the line where you wrote it. An expression (`const shout = function () {}`) is stored in a variable and only works after that line runs.

**What is an arrow function in JavaScript?** A shorter way to write a function: `const double = (n) => n * 2`. With a single expression as the body, the result is returned for you without the word `return`.

**What is the difference between parameters and arguments?** Parameters are the names in the function definition. Arguments are the real values you pass when you call it.

**Why does my JavaScript function return undefined?** Almost always the function has no `return`, or it is an arrow function with curly braces and no `return`. `console.log` shows a value but does not return it.

**When does a default parameter value apply?** Only when the argument is `undefined`, meaning nothing was passed. `null` and `0` are real values, so the default is ignored.

**What are rest parameters in JavaScript?** Three dots before the last parameter, like `...nums`. Every extra argument is collected into a real array, which is empty when nothing is passed.

**What is a callback function?** A function you pass to another function so that it can run it, like the arrow passed to `twice`. Functions are values, so passing them around is normal in JavaScript.

Next in the series: arrays.
