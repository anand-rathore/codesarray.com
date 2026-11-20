title: JavaScript files and JSON in Node: read, write and parse
summary: How a program remembers after it ends: pass words in with process.argv, read and write files with readFileSync and writeFileSync, turn objects into text with JSON.stringify and JSON.parse, see what JSON quietly drops, and build a notes tool that saves to a file. Four short programs with their real output.
description: JavaScript files and JSON in Node: process.argv, readFileSync, writeFileSync, JSON.stringify and JSON.parse, what JSON drops, and a notes tool, with real output.
date: 2026-11-20
read: 9 min read
lesson: 13
video: Files and JSON | https://youtu.be/9Llr0WvUSs8
image: cover.png
---
This lesson is about JavaScript files and JSON in Node: how a program keeps what it learned after it ends. By the end of this page you will pass words into a script with `process.argv`, read and write real files with `readFileSync` and `writeFileSync`, turn whole objects into text with `JSON.stringify` and back with `JSON.parse`, know exactly what JSON quietly drops, and build a small notes tool that remembers your notes for good.

## Why a program forgets

While your program runs, its variables live in memory. Memory is a whiteboard: fast and easy to change, and wiped clean the moment the program ends. Run the program again and the whiteboard is blank. A file is a notebook on the shelf. Writing in it is slower, but close the notebook, come back next year, and your words are still there, because a file lives on the disk. Every program that remembers follows the same plan. When it starts, it reads the notebook into memory. While it runs, it works on the whiteboard. Before it ends, it writes the whiteboard back into the notebook.

## process.argv: pass words into a script

You already run a script with `node file.js`. You can keep typing after the file name: `node notes.js add buy milk`. Those extra words are arguments, like the destination you tell a taxi driver as you get in: the taxi is the same every time, and the destination changes the trip. Your script finds them in `process.argv`, an array of strings. Position 0 is the path to Node itself, position 1 is the path to your script, and your own words start at index 2. That trips everyone up once: it is `process.argv[2]`, not `process.argv[0]`.

```js
console.log(process.argv[0]);
console.log(process.argv[1]);
console.log(process.argv[2]);

const name = process.argv[2] ?? "world";
console.log("hello, " + name);
```

Run as `node snippet.js`, the last two lines print `undefined` and `hello, world`. Run as `node snippet.js Ada`:

```output
C:\Program Files\nodejs\node.exe
C:\path\to\snippet.js
Ada
hello, Ada
```

The first two lines are paths on your own machine, so they will look different. The third is `Ada`, sitting at index 2. With no word typed, `process.argv[2]` is `undefined`, and the nullish operator `??` falls back to `"world"`.

## Read and write files with node:fs

Everything you need ships with Node, in the `node:fs` module. `writeFileSync(file, text)` takes the file name and the text to put in it. If the file does not exist, Node creates it. If it does exist, the old content is replaced, all of it: it does not add to the end, it rips the page out and writes a fresh one. `readFileSync(file, "utf8")` is the mirror. The `"utf8"` matters: a file on disk is really just bytes, and utf8 is the translator that turns them back into letters. Forget it and you get a `Buffer`, raw bytes. With it you get an ordinary string. To add a line to a file, read the old text, glue the new line on, and write the whole thing back.

```js
import { readFileSync, writeFileSync } from "node:fs";

writeFileSync("todo.txt", "buy milk\ncall mum\n");

const text = readFileSync("todo.txt", "utf8");
console.log(text);
console.log(typeof text, text.length);

const bigger = text + "water plants\n";
writeFileSync("todo.txt", bigger);
console.log(readFileSync("todo.txt", "utf8"));
```

```output
buy milk
call mum

string 18
buy milk
call mum
water plants

```

The file comes back exactly as it was written. `typeof text` is `"string"` and its length is 18 characters, counting the two new lines. After the glue and the second write, all three lines are there. The blank lines in the output are the final `\n` of each text plus the newline `console.log` adds.

## JSON: save whole objects as text

Real data is not text, it is objects and arrays: a player with a name and a score. You cannot hand an object to `writeFileSync`, which wants a string. JSON, short for JavaScript Object Notation, is a way to write a whole object as one piece of text. `JSON.stringify` packs your object into a string, like packing a box for a move. `JSON.parse` unpacks the box and rebuilds the object, keys, values and nesting. Stringify to save, parse to load. Two extra arguments, `null` and `2`, pretty print the text with line breaks and indents so a person can read the file too.

## What JSON drops

The box has rules. JSON can hold exactly six kinds of thing: objects, arrays, strings, numbers, booleans and `null`. A function cannot be written as text, so `stringify` drops it, silently. A value of `undefined` is dropped too: the whole key disappears from the string, with no error and no warning. A `Date` is turned into a plain string on the way out, and `parse` does not turn it back. A `Map` or a `Set` comes out as empty braces. Keep your saved data to those six and the round trip is perfect.

```js
const player = {
  name: "Ada",
  score: 120,
  level: undefined,
  greet() { return "hi"; },
};

const text = JSON.stringify(player, null, 2);
console.log(text);

const back = JSON.parse(text);
console.log(back.name, back.score);
console.log("level" in back, "greet" in back);
```

```output
{
  "name": "Ada",
  "score": 120
}
Ada 120
false false
```

`name` and `score` made it. `level` and `greet` are gone, with no error anywhere. The two questions at the end both come back `false`: the keys did not return empty, they were never packed at all.

## A notes tool: load, change, save

Every tool that saves data has the same shape, like a coin jar: take the jar down, drop a coin in, put the jar back. Load the file into an array, change the array, write the array back. The one wrinkle is the very first run, when there is no file yet and `readFileSync` throws. From the last lesson you know the answer: catch that error and start with an empty array.

```js
import { readFileSync, writeFileSync } from "node:fs";

function load() {
  try {
    return JSON.parse(readFileSync("notes.json", "utf8"));
  } catch {
    return [];
  }
}

const notes = load();
const command = process.argv[2];

if (command === "add") {
  const text = process.argv.slice(3).join(" ");
  if (text === "") {
    console.log("nothing to add");
  } else {
    notes.push(text);
    writeFileSync("notes.json", JSON.stringify(notes, null, 2));
    console.log("added:", text);
  }
} else if (command === "list") {
  if (notes.length === 0) {
    console.log("no notes yet");
  }
  notes.forEach((note, i) => console.log(i + 1 + ". " + note));
} else {
  console.log("usage: node notes.js add some text, or list");
}
```

`load()` reads `notes.json` and parses it in one move; if anything goes wrong, no file yet or broken JSON, the `catch` hands back an empty array, a fresh jar. `process.argv.slice(3).join(" ")` collects every word from index 3 on into one note, and the empty-text check guards the case where no words were typed. Here are four separate runs in a fresh folder, saved as `snippet_4.js`:

```output
> node snippet_4.js list
no notes yet
> node snippet_4.js add buy milk
added: buy milk
> node snippet_4.js add call mum
added: call mum
> node snippet_4.js list
1. buy milk
2. call mum
```

Each run started from nothing, loaded the file, and the notes were just there. Open `notes.json` and you can read it yourself, a tidy JSON array:

```output
[
  "buy milk",
  "call mum"
]
```

## Mistakes to avoid

- Forgetting `"utf8"` on `readFileSync`. You will know it when `console.log` shows the word `Buffer` and a row of numbers. Add the encoding and you get a string.
- Trusting `writeFileSync` to add to the end. It replaces the whole file, every time. Read, change, write back.
- Feeding `JSON.parse` something that is not JSON, like an empty or half-saved file. It throws a `SyntaxError`, so wrap any parse of a file in `try` and `catch`, like the notes tool does.
- Expecting `undefined` or a function to survive `JSON.stringify`. They will not, and you will not be told.
- Building file text by hand with plus signs when the data is really an object. Do not invent your own format: JSON is right there.

## What you learned

- Memory is wiped when the program ends; a file on disk is not, so a program that remembers loads at the start and saves at the end.
- `process.argv` is an array of strings: index 0 is Node, index 1 is your script, and your own words start at index 2.
- `readFileSync(file, "utf8")` turns a file into a string, and `writeFileSync(file, text)` turns a string into a file, replacing what was there.
- `JSON.stringify` packs an object into text, `JSON.stringify(x, null, 2)` makes it readable, and `JSON.parse` rebuilds the object.
- JSON keeps objects, arrays, strings, numbers, booleans and `null`, and silently drops functions and `undefined`.
- Load, change, save is the shape of every tool that remembers.

## Common questions

**What is the difference between readFileSync and readFile?** `readFileSync` stops the whole program until the file has been read, which is simple and fine for small scripts. The asynchronous versions let the program do other work while it waits; they come later in the track.

**Why does readFileSync return a Buffer?** Without an encoding, Node gives you the raw bytes. Pass `"utf8"` as the second argument to get a normal string.

**How do I append to a file instead of replacing it?** With `writeFileSync` you read the old text, add your new text to it, and write it all back, as in the todo program above. Node also has `appendFileSync` for exactly that job.

**Why does JSON.stringify leave out my keys?** JSON has no way to write a function or `undefined`, so keys holding them are dropped without an error. A `Date` becomes a string, and a `Map` or `Set` becomes `{}`.

**What does JSON.stringify(obj, null, 2) mean?** The `null` means keep every key, and the `2` means indent with two spaces, so the saved file is easy for a person to read.

Next lesson: the beginner capstone, a complete task tracker built from everything in this track.
