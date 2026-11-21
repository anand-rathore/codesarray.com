title: JavaScript project for beginners: build a task tracker CLI
summary: Build a complete task tracker for the command line in plain Node, using only arrays, objects, functions, JSON files and try/catch. Add tasks, mark them done, list them, keep them between runs, and report every mistake with a clear message. Two programs with their real output.
description: JavaScript project for beginners: build a task tracker CLI with Node using arrays, objects, JSON files, process.argv and try/catch, with real output.
date: 2026-11-21
read: 9 min read
lesson: 14
video: Task tracker CLI | https://youtu.be/ODXE8kA-VB4
image: cover.png
---
This lesson is a JavaScript project for beginners: a task tracker for the command line, built with Node from nothing. By the end of this page you will have a tool you can run as `node tasks.js add buy milk`, `node tasks.js done 1` and `node tasks.js list`, that keeps your tasks in a file between runs and answers every mistake with a clear message instead of a crash. You already know every piece: arrays, objects, functions, `process.argv`, JSON files, and `try` and `catch`.

## What we are building

Think of the to-do list stuck on your fridge. You write a task on it, you tick a task off, and you read the list. That is the whole app: three commands. `add` with some words writes a new task, `done` with a number ticks that task off, and `list` shows everything. Before writing any code, decide what a task looks like.

## The shape of the data

A task needs three facts: a number so you can point at it, a title, and whether it is done. Three facts with names is an object, for example `{ id: 1, title: "buy milk", done: false }`. A list of tasks is an array of those objects. Save that array with `JSON.stringify` and it lands in a file called `tasks.json`; load it back with `JSON.parse` and the array is there again. That design took thirty seconds and it is already done.

## The shape of the program

You have seen this one before: the coin jar. Take the jar down, drop a coin in, put it back. Load the file into an array, change the array, save the array back. This app talks to you, so there is one more step: show the list. Every command runs the same four steps, load, change, save, show, and only the change differs. `add` pushes a new object, `done` flips a done flag, and `list` changes nothing at all.

## Stage one: a tracker that rolls

Build it like a bike: make it roll first, add the brakes after. Stage one can add and list.

```js
import { readFileSync, writeFileSync } from "node:fs";

function load() {
  try {
    return JSON.parse(readFileSync("tasks.json", "utf8"));
  } catch {
    return [];
  }
}

const tasks = load();
const [command, ...words] = process.argv.slice(2);

if (command === "add") {
  const id = Math.max(0, ...tasks.map((t) => t.id)) + 1;
  tasks.push({ id, title: words.join(" "), done: false });
  writeFileSync("tasks.json", JSON.stringify(tasks, null, 2));
}

for (const t of tasks) {
  console.log(`${t.done ? "[x]" : "[ ]"} ${t.id}. ${t.title}`);
}
```

Lines 3 to 9 are `load`. It tries to read `tasks.json` and parse it; if that fails because there is no file yet, the `catch` hands back an empty array, a fresh list. Line 12 splits `process.argv`: `slice(2)` skips the Node path and the script path, the first word left is the command, and the rest syntax collects every other word into `words`. Line 15 makes the new id: `map` pulls out every id and `Math.max` finds the biggest, and the zero up front is for the empty list, so the first task gets id 1. Line 16 pushes a new object with the title built by joining the words and `done` set to `false`. Line 17 saves the whole array back as pretty JSON. Lines 20 to 22 print every task, with a ternary picking the check box: `[x]` for a done task and `[ ]` for one still to do.

Run it in a fresh folder. With no command there is no file and nothing to print. Then `add buy milk`, `add call mum`, and a run with no command at all:

```output
> node snippet.js
> node snippet.js add buy milk
[ ] 1. buy milk
> node snippet.js add call mum
[ ] 1. buy milk
[ ] 2. call mum
> node snippet.js
[ ] 1. buy milk
[ ] 2. call mum
```

The last run was a brand new run of the program, and both tasks were still there. Your tracker rolls. It has gaps, though: `add` with no title saves a task with an empty title, and there is no way to finish a task.

## What can go wrong

A real person will type `add` and forget the title. They will type `done` with a number that does not exist, a command the program has never heard of, or nothing at all. And one day the file itself will get broken. Every one of these is an error you can see coming, like a smoke alarm: it does not mean the house is on fire, it means someone burnt the toast. So the program should not crash. It throws a clear `Error` with a plain message where the problem is found, and catches it in one place, at the bottom, where it prints it nicely.

## Stage two: the whole app

```js
import { readFileSync, writeFileSync } from "node:fs";

function load() {
  try {
    return JSON.parse(readFileSync("tasks.json", "utf8"));
  } catch (err) {
    if (err instanceof SyntaxError) {
      throw new Error("tasks.json is broken", { cause: err });
    }
    return [];
  }
}

function run(tasks, command, words) {
  if (command === "add") {
    if (words.length === 0) {
      throw new Error("add needs a title");
    }
    const id = Math.max(0, ...tasks.map((t) => t.id)) + 1;
    tasks.push({ id, title: words.join(" "), done: false });
  } else if (command === "done") {
    const task = tasks.find((t) => t.id === Number(words[0]));
    if (!task) {
      throw new Error("no such task");
    }
    task.done = true;
  } else if (command !== "list") {
    throw new Error("use: add, done or list");
  }
}

try {
  const [command, ...words] = process.argv.slice(2);
  const tasks = load();
  run(tasks, command, words);
  writeFileSync("tasks.json", JSON.stringify(tasks, null, 2));
  const lines = tasks.map((t) => `${t.done ? "[x]" : "[ ]"} ${t.id}. ${t.title}`);
  console.log(lines.join("\n") || "no tasks yet");
} catch (err) {
  console.log("error:", err.message);
}
```

Lines 3 to 12 are `load` again, with one new idea. Line 7 asks whether the caught error is a `SyntaxError`, which is what `JSON.parse` throws on a broken file, and line 8 throws a new `Error` that keeps the original as its `cause`. The file holds your tasks: if the program quietly started from an empty list, the next save would wipe them out. Any other failure, like a missing file, is expected, so line 10 returns the empty list.

Lines 14 to 30 are a new function, `run`, which gets the tasks, the command and the words. Lines 16 to 18 guard the empty case: no words means `add needs a title`. Lines 19 and 20 are the same two lines as stage one. Line 21 starts the new `done` command. Line 22 uses `find` to look for the task whose id matches; `Number` turns the word you typed into a number, because everything from `process.argv` is a string. Lines 23 to 25 throw if `find` came back with nothing, and otherwise line 26 flips the flag. Line 27 catches the rest: if the command is not `list`, it is one the program does not know, and line 28 throws with a hint. `list` needs no code of its own: change nothing, show everything.

The main part, lines 32 to 41, runs inside one `try`. It splits `process.argv`, loads, runs the command, saves, builds one line of text per task with `map`, and prints them joined with new lines. If the list is empty, the join gives an empty string and the `||` operator falls back to `no tasks yet`. The `catch` on lines 39 to 41 is the one place every error lands, and it prints the word `error:` and the message. A `throw` from anywhere above jumps straight there, and it skips the save, so a bad command can never touch the file.

Run it, and break it on purpose:

```output
> node tasks.js list
no tasks yet
> node tasks.js add buy milk
[ ] 1. buy milk
> node tasks.js add call mum
[ ] 1. buy milk
[ ] 2. call mum
> node tasks.js done 1
[x] 1. buy milk
[ ] 2. call mum
> node tasks.js done 9
error: no such task
> node tasks.js add
error: add needs a title
> node tasks.js dance
error: use: add, done or list
```

Then damage the file so it is no longer JSON (here it holds only `{oops`) and list again:

```output
> node tasks.js list
error: tasks.json is broken
```

The file is still there exactly as it was. The program refused to overwrite it. Nothing crashed, and every mistake got a clear message.

## What you built

- The data is an array of objects, and every command is just a different way to change that array.
- All the file work lives in two places, `load` and the save line. Everything else only sees plain arrays and objects.
- Errors are thrown where they are found and caught in one place, which is why the code reads so clean.
- Saving only happens after the change worked, so if the change throws, the file stays safe. That is not a trick for tasks; it is how you write any program that keeps data.

## Your turn

Three upgrades, and you know everything you need for each. Add a `remove` command: use `filter` to keep every task that is not the one you want gone. Add a `clear` command that drops every done task: `filter` again. Show how many tasks are left at the bottom of the list: `filter` and `length`. Try them from what you know, without looking anything up. The first time you add a feature to your own code without a tutorial is when you stop learning JavaScript and start using it.

## What you learned

- A task is an object with an `id`, a `title` and a `done` flag, and the list is an array of those objects saved as `tasks.json`.
- The shape of every tool that remembers is load, change, save, show.
- `const [command, ...words] = process.argv.slice(2)` splits the command from its words, and every word is a string.
- `find` looks up a task, `push` adds one, `map` builds the text, and `Math.max(0, ...ids) + 1` makes the next id.
- `throw new Error(...)` reports a mistake where it is found, and one `try` and `catch` at the bottom catches them all.
- A broken `tasks.json` is reported, with `instanceof SyntaxError` and a `cause`, instead of being overwritten.

## Common questions

**How do I build a task tracker in JavaScript?** Store each task as an object with an id, a title and a done flag, keep them in an array, and save the array to a JSON file with `JSON.stringify`. Each command loads the file, changes the array, saves it and prints the list.

**Why does the first task get id 1?** `Math.max(0, ...tasks.map((t) => t.id))` is `0` for an empty list, and the code adds 1. Without the zero, `Math.max()` of nothing is `-Infinity`.

**Why use Number(words[0]) in the done command?** Every value in `process.argv` is a string, and the ids in the file are numbers. `find` compares with `===`, so `"1"` would never match `1` until `Number` converts it.

**Why does a broken tasks.json throw instead of starting a fresh list?** The file holds your data. If `load` returned an empty list for a broken file, the next save would overwrite your tasks with nothing. Only a missing file is safe to treat as empty.

**Why does the save come after the command runs?** A `throw` in `run` jumps to the `catch` and skips the save, so a bad command never changes the file.

Next lesson: the Intermediate track starts with Big O in JavaScript, how to tell whether your code is fast before you run it.
