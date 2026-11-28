title: JavaScript this keyword explained: 4 rules, bind, prototypes
summary: Learn the JavaScript this keyword with the four binding rules: why a saved method prints undefined, how call, apply and bind choose this, why arrows have none, and how the prototype chain shares methods, with real Node output.
description: JavaScript this keyword explained with real Node output: the four binding rules, call, apply and bind, arrow functions, and the prototype chain.
date: 2026-11-28
read: 7 min read
lesson: 3
video: Why JavaScript Methods Lose this (and How to Fix It) | https://youtu.be/69hVO-X0XhM
image: cover.png
---
JavaScript this keyword explained: this page shows why the same function can answer with a different owner on every call, and how objects share methods through the prototype chain. By the end you will know the four rules that set `this`, how `call`, `apply` and `bind` work, why arrow functions have no `this` of their own, and what `prototype` and `__proto__` really are. Everything here ran on Node 24.

## The puzzle: where did Ada go?

```js
function hello() {
  return `Hi, I'm ${this?.name}`;
}

const ada = { name: "Ada", hello };

console.log(ada.hello());

const loose = ada.hello;
console.log(loose());
```

```output
Hi, I'm Ada
Hi, I'm undefined
```

`ada.hello()` knows Ada's name. Save the very same function into a variable and call it bare, and the name is gone. Nothing about the function changed. Only the call did: there is no `ada.` in front anymore. That missing dot is the whole story of `this`.

## this is decided at the call

Inside a function, `this` is a hidden extra value: the object the function is working for, this time. Think of the word "my". When Ada says "my phone", it is Ada's phone; when Ben says it, the same word means a different phone. The word does not own anything, the speaker does. So the question is never "what is `this` in this function?" It is "who is calling it, this time?"

## The four rules

There are only four ways to call a function, and each one sets `this`.

1. **A method call**: `ada.hello()`. Look left of the dot; that object is `this`.
2. **A plain call**: `loose()`. Nobody is left of the dot. In a module or strict mode `this` is `undefined`; in an old-style script it falls back to the global object. Either way, it is not Ada.
3. **An explicit call**: `hello.call({ name: "Zoe" })` prints `Hi, I'm Zoe`. You hand the function the `this` you want, yourself.
4. **new**: `new User("Mia")` builds a brand-new object and runs `User` with `this` pointing at it.

When `this` surprises you, find the call and ask: which rule is this?

## call, apply, bind, and the callback trap

```js
function describe(role, city) {
  return `${this.name}, ${role}, from ${city}`;
}

const ada = { name: "Ada" };

console.log(describe.call(ada, "developer", "Pune"));
console.log(describe.apply(ada, ["developer", "Pune"]));

const describeAda = describe.bind(ada);
console.log(describeAda("writer", "Goa"));

function runTwice(job) {
  job();
  job();
}

const counter = {
  count: 0,
  startBroken() {
    runTwice(function () { this.count += 1; });
  },
  start() {
    runTwice(() => { this.count += 1; });
  },
};

counter.startBroken();
console.log(counter.count);

counter.start();
console.log(counter.count);
```

```output
Ada, developer, from Pune
Ada, developer, from Pune
Ada, writer, from Goa
0
2
```

`call` takes the owner first, then the arguments one by one. `apply` is the same with the arguments packed in one array (remember it as "a for array"). `bind` calls nothing: it returns a new function with `this` glued on permanently, and that function still takes fresh arguments every time.

Now the trap. `startBroken` ran its job twice, yet `counter.count` is still `0`. The job is an old-style function, and `runTwice` calls it plain: no dot, rule two. In an old-style script `this` falls back to the global object, so both `+= 1` landed on a variable nobody will ever read; in a module it throws `TypeError: Cannot read properties of undefined` instead. The fix is the arrow in `start`: an arrow has no `this` of its own, so it uses `start`'s `this`, the counter, and the count goes 0, 1, 2. That is also why an arrow is exactly the wrong choice as a method: its `this` is whatever was outside the object.

## The prototype chain

```js
const animal = {
  describe() {
    return `${this.name} says ${this.sound}`;
  },
};

const dog = Object.create(animal);
dog.name = "Rex";
dog.sound = "woof";

console.log(dog.describe());
console.log(Object.getPrototypeOf(dog) === animal);
console.log("describe" in dog);
console.log(Object.hasOwn(dog, "describe"));
```

```output
Rex says woof
true
true
false
```

`dog` has a name and a sound, and no `describe` anywhere. The call still works because every object has a hidden link to another object, its prototype. Ask an object for something it does not have, and the lookup follows the link and asks the prototype, then that object's prototype, up the chain until it finds an answer or hits `null`. `Object.create(animal)` builds that link directly. The method came from `animal`, the name came from `dog`, and `this` stitched them together: `"describe" in dog` is `true` because it is reachable, while `Object.hasOwn(dog, "describe")` is `false` because `dog` never owned it.

One caution: the chain only answers reads. Writes always land on the object itself, so writing `dog.describe = ...` quietly covers the shared method.

## prototype vs __proto__

```js
function User(name) {
  this.name = name;
}

User.prototype.hello = function () {
  return `Hi, I'm ${this.name}`;
};

const mia = new User("Mia");
const leo = new User("Leo");

console.log(mia.hello());
console.log(leo.hello());
console.log(Object.getPrototypeOf(mia) === User.prototype);
console.log(mia.hello === leo.hello);
console.log(mia instanceof User);
```

```output
Hi, I'm Mia
Hi, I'm Leo
true
true
true
```

These two names trip everyone. `__proto__` is the hidden link every object has; the polite way to read it is `Object.getPrototypeOf`. `prototype` is a property only functions have, and it is not the function's own link: it is the object that `new` will hand out as the link to everything the function builds. Think of a bakery: `User` is the baker, `User.prototype` is the recipe book on the shelf, and every loaf `new User` bakes gets a tag pointing back at that shelf. Put `hello` on the shelf once and `mia.hello === leo.hello` is `true`: one function in memory, shared by every user you build. `instanceof` only asks whether `User.prototype` appears anywhere up the object's chain.

Two warnings. If a function is a builder, always call it with `new`: forget it and `this` is `undefined`, so nothing gets built and a module crashes. And never assign to `__proto__` directly: changing an object's prototype after it is built is one of the slowest things you can do to it. Link objects when you create them, with `Object.create` or classes.

## One last test

`counter.start` uses an arrow inside, and it worked above. Now run `const tick = counter.start; tick();`. Does the arrow save it again? No: the count stays at `0`, and in a module it crashes. The arrow borrows `this` from `start`, and this time `start` itself was called plain, so there was nothing to borrow. Rules first, arrows second.

## What you learned

- `this` is set at every call, not when the function is written: find the call, look left of the dot.
- The four rules: method call, plain call, explicit `call`/`apply`/`bind`, and `new`.
- `bind` returns a new function with `this` glued on; arrows have no `this` and borrow it from where they were written.
- Every object has a prototype link; lookups walk up the chain, writes land on the object itself.
- `prototype` lives on functions and is handed out by `new`; `__proto__` is the link on every object.

## Common questions

**Why does my method print undefined after I save it to a variable?** Because the call lost its dot. A plain call has no owner, so `this` is `undefined` in modules and strict mode. Fix it with `const f = obj.method.bind(obj)` or call it through an arrow: `() => obj.method()`.

**Should methods be arrow functions?** No. An arrow in an object literal does not see the object; its `this` is whatever was outside. Use normal functions for methods, and arrows for the callbacks inside them.

**What is the difference between call and apply?** Only the shape of the arguments: `fn.call(owner, a, b)` takes them one by one, `fn.apply(owner, [a, b])` takes one array.

**Is __proto__ the same as prototype?** No. `__proto__` is the hidden link every object has (read it with `Object.getPrototypeOf`). `prototype` exists only on functions and becomes the `__proto__` of objects made with `new`.

**Does instanceof check the class name?** No. `x instanceof F` only asks whether `F.prototype` appears anywhere up `x`'s prototype chain.

Next lesson: classes, the same builder-plus-prototype pattern you just learned, written with class syntax.
