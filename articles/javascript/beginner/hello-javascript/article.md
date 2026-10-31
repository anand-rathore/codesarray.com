title: JavaScript for beginners: your first program, step by step
summary: See what JavaScript actually is, run it in the browser console and with Node.js, and read a thirteen-line program one line at a time.
description: JavaScript for beginners: run your first program in the browser console and with Node.js, and learn console.log, let vs const and typeof.
date: 2026-10-31
read: 6 min read
lesson: 1
video: Hello, JavaScript | https://youtu.be/yoKc48x9xyY
image: cover.png
---
This is JavaScript for beginners, the first lesson in the track, and it assumes you have never written a line of code. By the end of this page you will know what JavaScript actually is, you will have run it in two different places, and you will have read a real thirteen-line program one line at a time.

## What JavaScript actually is

Every time a web page does something, JavaScript did it. You tap a like button and the count goes up without the page reloading? That's JavaScript. You type a wrong password and the box shakes? JavaScript. A streaming site starts a preview when you hover over a movie? JavaScript again.

It is the language that makes web pages do things, and it is running in your browser right now. These days it has gone well past the browser: the same language runs on servers, in phone apps and in desktop apps. One language, running nearly everywhere, which is exactly what makes it a great first language to learn.

## Two places to run it

The first one you already have. In your browser, on almost any page, press **F12** and click the tab that says **Console**. That is a JavaScript playground hiding inside your browser. Type `2 + 3`, press enter, and it answers `5` instantly.

The second place is Node.js, which runs JavaScript directly on your computer, no browser needed; it is how people use JavaScript to build servers and tools. Go to [nodejs.org](https://nodejs.org/), download the LTS version and install it. Then check it worked:

```
node --version
```

```output
v24.21.0
```

If you see a version number like 24, you are ready.

## Two small tools before the code

The first tool is `console.log`. It prints things on the screen: think of it as your program's receipt printer, because whatever you hand it, it prints.

The second tool is variables. A variable is a labelled box with a value inside, and JavaScript gives you two ways to make one. Imagine you are at an ice cream shop. The number of scoops you want might change, so it goes in a box made with `let`. The price per scoop was decided by the shop and you do not get to change it, so it goes in a box made with `const`, short for constant. That is the whole rule: `let` is for things that can change, `const` is for things that can't. When in doubt, start with `const`.

## The program

Save this as `hello.js`:

```javascript
// my first JavaScript program
console.log("Hello, World!");

let scoops = 2;    // can change
const price = 3.5; // locked

console.log("Scoops:", scoops);
console.log("Total:", scoops * price);

scoops = 3; // changed my mind
console.log("New total:", scoops * price);

console.log(typeof scoops, typeof "hello", typeof true);
```

Line by line:

- **Line 1** is a comment. The two slashes tell JavaScript to skip the line completely; it is a note for humans.
- **Line 2** prints `Hello, World!`. Almost every programmer on earth started with this exact line.
- **Line 4** makes a box called `scoops` with `let`, holding the number 2.
- **Line 5** makes the `price` box with `const`: 3.5 per scoop, locked.
- **Lines 7 and 8** print the order. `console.log` can take several things at once, and it can do the maths right there inside the brackets: `scoops * price`.
- **Line 10** changes our mind at the counter. Because `scoops` was made with `let`, JavaScript happily swaps the 2 for a 3.
- **Line 11** runs the exact same maths as line 8, but the answer will be different, because the box has a new value in it.
- **Line 13** asks `typeof` about three different values at once.

## Run it

In the terminal, in the folder where you saved the file:

```
node hello.js
```

```output
Hello, World!
Scoops: 2
Total: 7
New total: 10.5
number string boolean
```

Two scoops at 3.5 is 7; after line 10 the same line of code prints 10.5. And look at the last line: `number`, `string`, `boolean`. Nobody told JavaScript any of that. You just put values in the boxes and it worked out what each one was: 2 is a number, `"hello"` in quotes is a string (the programmer word for text), and `true` and `false` are booleans, the yes-or-no values. `typeof` in front of any value tells you its kind.

## What you learned

- JavaScript is the language that makes web pages do things, and with Node it runs anywhere.
- The browser console (F12) is a JavaScript playground you already have.
- `node hello.js` runs a file.
- `console.log(...)` prints whatever you give it.
- `//` starts a comment, a note for humans.
- `let` makes a box you can change; `const` makes one that's locked.
- `typeof` tells you what kind of value you are looking at.

## Common questions

**Do I need to learn HTML and CSS first?** No. HTML and CSS describe what a page looks like; JavaScript is the programming language, and this series teaches it on its own with Node. When you later build pages, the JavaScript you learn here carries straight over.

**Which should I install, Node's LTS or Current version?** LTS, which stands for long-term support. It is the stable line that most companies run (Node 24 as of this lesson), and every example in this series works on it.

**What happens if I try to change a `const`?** The program stops with an error: `TypeError: Assignment to constant variable.` That is a feature, not a problem. It catches accidental changes to things that were never supposed to change.

**Why did `typeof` say `number` for 2 and not integer?** JavaScript has one number type for whole numbers and decimals alike, so 2 and 3.5 are both simply `number`. Other languages separate integers from decimals; JavaScript does not.

**Do the semicolons matter?** JavaScript can usually guess where a line ends without them, but the guessing has famous edge cases. Ending each statement with a semicolon, the way this lesson does, is the habit that never surprises you.

Next in the series: variables and types.
