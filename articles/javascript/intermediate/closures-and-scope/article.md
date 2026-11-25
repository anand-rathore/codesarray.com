title: JavaScript closures and scope explained: counters, let vs var
summary: Learn JavaScript closures and scope: how a function remembers variables, counters and function factories, why a var loop gives 3, 3, 3, and private data with the module pattern, with real output from Node.
description: JavaScript closures and scope explained with real Node output: the scope chain, counters, function factories, the var loop bug and the module pattern.
date: 2026-11-25
read: 8 min read
lesson: 2
video: Closures and Scope in JavaScript | https://youtu.be/OKirj2Q_5xw
image: cover.png
---
JavaScript closures and scope explained: this page shows how a function can keep using the variables around it, even after the function that made them has finished. By the end you will know where a variable can be seen, what a closure really is, how to build counters and function factories, why a `var` loop gives `3, 3, 3`, and how to keep data private with the module pattern. Everything here ran on Node 24.

## Start with a puzzle

Two counters come from the same function, `makeCounter`. Call `a()` twice and you get `1`, then `2`. Now call `b()`. Does it print `1` or `3`? It prints `1`. Each counter keeps its own `count`, even though `makeCounter` finished running long ago. That is a closure, and the rest of this page explains why it works.

## What scope is

Scope means where a variable can be seen. Picture a room with a window: from inside you can see the garden, but from the garden you cannot see inside. A function is a room. Variables made inside it belong to it, and code outside cannot see them, while code inside can look outward at everything around the function.

There are three levels: global scope, which is the outside of everything; function scope, inside one function; and block scope, inside any pair of curly braces. `let` and `const` live in the block they are written in, and when the block ends they are gone. Reading one afterwards gives `ReferenceError: inner is not defined`.

## Lexical scope and the scope chain

When JavaScript needs a variable, it looks in the current scope first. If it is not there, it steps outward to the scope around it, then the next one, until it reaches the global scope. If it is still not found you get a `ReferenceError`. That chain of scopes is the scope chain.

JavaScript uses lexical scope, which means the chain is decided by where you wrote the code, not by where you call the function. Look at the code and you can tell which variables a function can see: an inner function sees the outer one, never the other way around.

## What a closure is

Normally, when a function finishes, its variables are thrown away. But when an inner function is handed back out, it carries with it every variable it could see at the place where it was written, like a backpack. A closure is a function plus the variables around it that it still remembers. In fact every function in JavaScript is a closure; we only notice when one leaves the place it was born.

## A counter that remembers

`makeCounter` creates a variable, `count`, set to zero, and returns a small function that adds one to it. When `makeCounter` has finished running, the function it returned can still read and update `count`. Each call to `makeCounter` makes a fresh `count`, so two counters never touch each other.

```js
const site = "Codesarray";

function greet(name) {
  const greeting = "Hello";
  return `${greeting}, ${name}, from ${site}`;
}

function makeCounter() {
  let count = 0;
  return function () {
    count += 1;
    return count;
  };
}

const first = makeCounter();
const second = makeCounter();

console.log(greet("Ana"));
console.log(first(), first(), first());
console.log(second());
```

```output
Hello, Ana, from Codesarray
1 2 3
1
```

`greet` shows the scope chain: it finds `greeting` inside itself and `site` one level out. `first` is called three times and prints `1 2 3`. `second` comes from a separate call to `makeCounter`, so it starts again and prints `1`.

## Function factories

A function that builds other functions is a factory. `makeAdder(n)` returns a new function that adds `n` to anything, and the `n` stays in its backpack. `makeAdder(10)` gives you `addTen`, and `makeAdder(1)` gives you a function that adds one. The same idea builds a greeter for one language, a tax calculator for one country, or a handler for one button: fix a value now, use it later.

## The var in a loop bug

Loop three times, and each time save a small function that returns the counter. You would expect `0, 1, 2`. With `var` you get `3, 3, 3`, because `var` does not make a new variable for each trip around the loop: there is one `i` for the whole function, and by the time the functions run it has reached `3`. With `let`, each trip gets its own `i`, so each function keeps its own value.

```js
const makeAdder = (n) => (x) => x + n;
const addTen = makeAdder(10);
console.log(addTen(5), makeAdder(1)(5));

const oldWay = [];
for (var i = 0; i < 3; i++) {
  oldWay.push(() => i);
}
console.log(oldWay.map((fn) => fn()));

const newWay = [];
for (let j = 0; j < 3; j++) {
  newWay.push(() => j);
}
console.log(newWay.map((fn) => fn()));
```

```output
15 6
[ 3, 3, 3 ]
[ 0, 1, 2 ]
```

The first line is `makeAdder` at work: `addTen(5)` is `15` and `makeAdder(1)(5)` is `6`. The second line is the `var` loop and the third is the `let` loop. The only difference is one word.

## IIFEs

An IIFE, an immediately invoked function expression, is a function wrapped in brackets and called right away. It runs once and nothing inside leaks out. Before block scope existed, this was how people made a private room, and you still meet it in older code.

## The module pattern

The module pattern uses an IIFE and a closure to keep data private. Think of a vending machine: you can put coins in and read the display, but you cannot reach inside and change the total. Here `balance` is a plain variable inside the IIFE. `deposit` changes it after checking the amount, and the returned object shares only `deposit` and a getter for `balance`.

```js
const wallet = (function () {
  let balance = 0;

  function deposit(amount) {
    if (amount <= 0) {
      throw new RangeError("Deposit must be positive");
    }
    balance += amount;
    return balance;
  }

  return {
    deposit,
    get balance() {
      return balance;
    },
  };
})();

console.log(wallet.deposit(50));
console.log(wallet.deposit(25));
console.log(wallet.balance);
wallet.balance = 1000000;
console.log(wallet.balance);
console.log(wallet.deposit(5));
try {
  wallet.deposit(-5);
} catch (e) {
  console.log(e.name + ": " + e.message);
}
```

```output
50
75
75
75
80
RangeError: Deposit must be positive
```

The assignment `wallet.balance = 1000000` does nothing, so the balance stays `75`. In a script like this the assignment is silently ignored. In strict mode, which classes and modules use, assigning to a property that has only a getter throws a `TypeError` instead. Either way the balance stays safe, and a deposit of `-5` is refused with a `RangeError`. The only way in is through the door you built.

## Things to keep in mind

- A closure keeps the variable, not a copy of its value. If something changes the variable later, the function sees the new value.
- A closure keeps what it references in memory for as long as the function lives, so a closure holding a huge array keeps that array too.
- Use `let` in loops and let the language make a fresh variable each time.
- Shadowing, an inner variable with the same name as an outer one, is legal but confusing. Pick different names.

## What you learned

- Scope is where a variable can be seen: global, function and block.
- Scope is lexical: it is decided by where you wrote the code, and lookups follow the scope chain outward.
- A closure is a function plus the variables around it, and each call makes a new one, so counters and factories keep their own state.
- In a loop, `var` shares one variable and `let` makes a new one each trip.
- An IIFE plus a closure gives you private data, which is the module pattern.

## Common questions

**What is a closure in JavaScript?** It is a function together with the variables from the place where it was written. The function can keep reading and updating those variables even after the outer function has finished.

**Is every function a closure?** Yes, every function in JavaScript closes over the scope it was created in. You only notice it when the function is used somewhere else, such as when it is returned from another function.

**Does a closure copy the variable?** No. It keeps the variable itself. With `let x = 1; const read = () => x; x = 2;` calling `read()` returns `2`.

**Why does a `var` loop print `3, 3, 3`?** `var` creates one variable for the whole function, so every function you save in the loop shares it, and it ends at `3`. `let` creates a fresh variable for every trip around the loop, which gives `0, 1, 2`.

**How do closures make data private?** Variables inside a function cannot be reached from outside. If you return only the functions that are allowed to use them, as in the `wallet` example, the rest of the program can use the data only through those functions.

Next lesson: this and prototypes, why the same function can mean different things depending on how you call it.
