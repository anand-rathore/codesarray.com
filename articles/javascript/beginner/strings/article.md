title: JavaScript strings: template literals, slice, split, replaceAll
summary: Build sentences with backticks, why a string never changes in place, indexing and slice, why a thumbs up emoji has length 2, trim, split, includes, replaceAll, padStart, for...of and comparing text. Two short programs with their real output.
description: JavaScript strings for beginners: template literals, immutability, slice and at(-1), trim, split, includes, replaceAll, padStart, for...of, and why an emoji has length 2.
date: 2026-11-03
read: 10 min read
lesson: 4
video: Strings | https://youtu.be/nCEj9HYoRFE
image: cover.png
---
This lesson is about JavaScript strings: the text your programs read, build and compare. By the end of this page you will build sentences with backticks instead of gluing pieces together, you will know why a string can never be changed in place and what to do instead, you will pull pieces out of text, search it, clean it up and compare it, and you will know why a single thumbs up emoji has a length of 2.

## What a string is, and template literals

A string is a piece of text between quotes. Double quotes or single quotes both work, as long as you open and close with the same kind. Think of a name tag at a cafe: `"Maya"` is a string.

Say you want the sentence "Maya wants 2 flat whites". You could glue the pieces together with `+`, but it gets messy fast, with quotes and plus signs everywhere, and one missing space ruins it. There is a nicer way: backticks. A string written between backticks is a template literal, and wherever you want a value you write `${` then the value then `}`. Picture a form letter that says "Dear blank": JavaScript fills in the blank for you.

Anything can go inside the braces. `${cups * 3.5}` is worked out, and the answer lands in the sentence. A template literal can also run over several lines, and the line breaks stay. Use backticks any time you are mixing text with values.

## Strings can't be changed

Strings are immutable. Think of a laminated menu: you can read it, photograph it and copy it, but you cannot write on it. Try `text[0] = "M"` and JavaScript does not complain, it quietly ignores you, and `text[0]` is still a small `"m"`.

So how do you change a string? You make a new one. Every string method gives you a brand new string and leaves the old one alone: `text.toUpperCase()` gives a loud copy, and `text` itself is still in small letters. This is the number one beginner mistake: writing `text.toUpperCase()` on its own line makes a loud copy and throws it away. If you want the new string, save it in a new `const`, or put it back in the same variable if that one is a `let`. Every method in the rest of this page works this way.

## Indexing, length and slice

Picture a row of lockers with one letter in each, numbered from zero. `"Maya"[0]` is `"M"`, `"Maya"[1]` is `"a"`, and `"Maya".length` is 4, so the last letter is at index 3, one less than the length. Spaces count too: a space is a character and takes a locker.

To get the last character without any math, use `.at(-1)`. Minus one is the last, minus two the one before it. Ask for an index past the end, like `text[99]`, and JavaScript does not crash: it gives you `undefined`.

To take a piece, use `slice(start, stop)`. It stops just before the second number, so `slice(0, 4)` takes the characters at 0, 1, 2 and 3. Leave out the second number and it goes to the end. A negative number counts from the back: `slice(-6)` is the last six characters. And slice gives you a new string; the original stays as it was.

## Why a thumbs up emoji has a length of 2

`"👍".length` is `2`. It is one picture, so why two? JavaScript stores text in small fixed-size boxes called UTF-16 code units. Letters like a, b and c fit in one box, but there are well over 100,000 symbols in the world, emoji and many other alphabets, and some of them do not fit, so a thumbs up takes two boxes side by side. `length` counts boxes, not pictures, and `"👍"[0]` gives you half an emoji.

To count real characters, put three dots in front of the string inside square brackets: `[..."👍"].length` is `1`. For ordinary English text you will never notice any of this, but the moment a user types an emoji or a name in another alphabet, you will be glad you know.

## The string toolbox

Picture a till receipt. These methods are how you tidy it up, and every one of them returns a new string.

- `trim()` cuts the spaces off both ends. People leave spaces at the start and end of what they type, so use it on every text box.
- `split(",")` cuts a string into a list of pieces wherever it sees the separator. `"latte,mocha,tea,latte".split(",")` gives a list of four items.
- `includes("tea")` asks whether that piece is anywhere in the string and gives `true` or `false`. `startsWith` and `endsWith` check only the beginning or the end.
- `replaceAll("latte", "flat white")` changes every match. The plain `replace` changes only the first match, which catches people out, so use `replaceAll` when you mean all.
- `padStart(3, "0")` adds filler to the front until the string reaches that length: `"7".padStart(3, "0")` is `"007"`, perfect for order numbers. `padEnd` does the same at the back.
- `toUpperCase()` and `toLowerCase()` change the letters.

Because each one hands back a string, you can chain them: `trim()`, then `toLowerCase()`, then `split()`, in one line.

## Looping over a string

To look at each character in turn, use `for...of`. In `for (const ch of "hi👍")` the body runs once per character, with `ch` holding the current one: `"h"`, then `"i"`, then the whole thumbs up as one character. `for...of` walks through real characters, not boxes, so it is the safe way to loop over any text, emoji included. A classic counting loop up to `length` walks the boxes and would cut the thumbs up in half.

## Comparing strings

`===` compares the letters, not where the strings live in memory, so `"apple" === "apple"` is `true`. It is strict about case: `"apple" === "Apple"` is `false`. To ignore case, change both sides to lower case first, then compare.

`<` and `>` work on strings too. JavaScript compares like a dictionary, character by character, so `"apple" < "banana"` is `true`. But it compares characters, not numbers: `"10" < "9"` is `true`, because `"1"` comes before `"9"`. Never use `<` to compare numbers stored as text; turn them into real numbers first with `Number`.

The same trap shows up in sorting: capital letters sort before every small letter, so `["b", "a", "C"].sort()` puts `"C"` first. When you sort people's names, use `localeCompare`, which follows the rules of a real dictionary and gives a negative number, zero or a positive number, exactly what `sort` wants.

## The cafe order program

```javascript
// a cafe order, typed by a customer
const typed = "  maya wants 2 flat whites  ";
const text = typed.trim();
console.log(text);
console.log(text.length);

console.log(text[0], text.at(-1));
console.log(text.slice(0, 4));
console.log(text.slice(-6));
console.log(text[99]);

text[0] = "M";
console.log(text[0]);
const loud = text.toUpperCase();
console.log(loud);
console.log(text);

const cups = 2;
const name = text.slice(0, 4);
const nice = name[0].toUpperCase() + name.slice(1);
console.log(`${nice} wants ${cups} flat whites: ${cups * 3.5} dollars`);
console.log("👍".length, [..."👍"].length);
```

```output
maya wants 2 flat whites
24
m s
maya
whites
undefined
m
MAYA WANTS 2 FLAT WHITES
maya wants 2 flat whites
Maya wants 2 flat whites: 7 dollars
2 1
```

Line 3 trims what the customer typed, and line 5 prints its length, 24. Line 7 prints the first character and the last one with `at(-1)`. Lines 8 and 9 slice the first four letters and the last six, and line 10 asks for a character that is not there. Line 12 tries to change the first letter and is ignored, which line 13 proves. Line 14 makes a loud copy with `toUpperCase`, and line 16 shows the original unchanged. Line 20 makes a proper name by gluing a capital letter onto the rest, line 21 is the template literal with the price worked out inside it, and line 22 shows the length of a thumbs up before and after spreading.

## The till receipt program

```javascript
// cleaning up a till receipt
const sold = "latte,mocha,tea,latte";
const items = sold.split(",");
console.log(items);
console.log(sold.includes("tea"), sold.includes("chai"));
console.log(sold.replaceAll("latte", "flat white"));
console.log(sold.startsWith("latte"));

console.log("7".padStart(3, "0"), "tea".padEnd(6, ".") + "3.50");

for (const ch of "hi👍") {
  console.log(ch);
}

console.log("apple" === "apple", "apple" === "Apple");
console.log("apple".toLowerCase() === "Apple".toLowerCase());
console.log("apple" < "banana", "10" < "9");
console.log(["b", "a", "C"].sort(), "a".localeCompare("b"));
```

```output
[ 'latte', 'mocha', 'tea', 'latte' ]
true false
flat white,mocha,tea,flat white
true
007 tea...3.50
h
i
👍
true false
true
true true
[ 'C', 'a', 'b' ] -1
```

Line 3 splits the sales list on the commas. Line 5 asks `includes` for `"tea"` and for `"chai"`, and line 6 replaces every `"latte"`. Line 9 pads a 7 with zeros and pads the word `tea` with dots. Lines 11 to 13 are the `for...of` loop, one character per turn, with the thumbs up coming out whole. Lines 15 and 16 compare with `===`, first exactly and then after lower-casing both sides. Line 17 shows `"10" < "9"` is `true`, and line 18 sorts three letters and asks `localeCompare` to compare `"a"` and `"b"`.

## What you learned

- A string is text in quotes, and backticks with `${}` build sentences.
- Strings can't be changed, so every method gives you a new one: save the result.
- Index from zero, use `at(-1)` for the last character, and remember `slice` stops just before its second number.
- `length` counts UTF-16 boxes, so a thumbs up emoji is 2; `for...of` and `[...text]` give real characters.
- `trim`, `split`, `includes`, `replaceAll` and `padStart` do most of the cleaning.
- Compare with `===`, and lower-case first when case should not matter.

## Common questions

**Why does `name.toUpperCase()` not change my variable?** Strings are immutable, so a method cannot change them in place. It returns a new string, and if you do not save it, it is thrown away. Write `const loud = name.toUpperCase()`, or `name = name.toUpperCase()` if `name` is a `let`.

**What is the difference between `replace` and `replaceAll`?** `replace` changes only the first match, and `replaceAll` changes every match. When you mean "all of them", use `replaceAll`.

**Why is `"👍".length` equal to 2?** JavaScript counts UTF-16 code units, and an emoji like the thumbs up needs two of them. Use `[...text].length` or a `for...of` loop to work with whole characters.

**Why is `"10" < "9"` true?** Strings are compared one character at a time, like a dictionary, and `"1"` comes before `"9"`. Convert numbers stored as text with `Number` before comparing them.

**How do I compare two strings without caring about case?** Lower-case both sides, then compare: `a.toLowerCase() === b.toLowerCase()`. For sorting names the way a dictionary does, use `localeCompare`.

Next in the series: conditionals and logic.
