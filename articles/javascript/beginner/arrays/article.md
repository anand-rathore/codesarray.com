title: JavaScript arrays: index, push, pop, slice, splice and copy
summary: How you keep many values in one ordered list: creating an array, reading items by index, length, push, pop, shift and unshift, splice and slice, why equals does not copy an array, includes and indexOf, destructuring, and why a const array can still change. Three short programs with their real output.
description: JavaScript arrays for beginners: index, length, push, pop, shift, unshift, splice, slice, copying with spread, includes, indexOf and destructuring.
date: 2026-11-10
read: 11 min read
lesson: 8
video: Arrays | https://youtu.be/LkqP8qiUe44
image: cover.png
---
This lesson is about JavaScript arrays: how you keep many values in one ordered list. By the end of this page you will make an array and read any item by its number, add and remove items at the back and at the front, cut out a piece with `slice` and edit the middle with `splice`, make a real copy and see why a plain equals sign does not, search with `includes` and `indexOf`, unpack values with destructuring, and know why a `const` array can still change.

## Why arrays

Picture a row of lockers in a school hallway. Each locker has a number, they sit in order, and each one holds something. That is an array: one name, many values, in order.

Say you want to keep the names of five friends. You could make five variables, but what if there are fifty, or you do not know how many yet? An array is one variable holding a whole list. You write it with square brackets, with the items inside, separated by commas. It can hold any kind of value, text, numbers, even other arrays, and the order is kept: the first item you put in is the first item you get out.

## Creating an array

```javascript
const fruits = ["apple", "banana", "cherry"];
```

That is three strings in a list. An empty pair of square brackets, `[]`, is an empty array, a good place to start when you are going to fill it up. Print an array with `console.log` and you see the whole list. `typeof fruits` says `"object"`, which is a bit odd, so when you need to ask whether something is really an array, use `Array.isArray(fruits)`. It gives `true` or `false`.

## Index: reading and changing items

Every item has a number, called its index, and the count starts at zero. In `fruits`, `"apple"` is at index 0, `"banana"` is at 1, and `"cherry"` is at 2. To read an item, write the array name and the index in square brackets: `fruits[0]` is `"apple"`. To change an item, put that on the left of an equals sign: `fruits[1] = "blueberry"` replaces `"banana"`.

Ask for a spot that does not exist, like `fruits[5]`, and there is no error. You just get `undefined`. That is JavaScript being relaxed again, so if you get `undefined`, check your index.

## length and at(-1)

Every array knows how many items it has. It is called `length`, so `fruits.length` is `3`. There are no brackets after `length`, because it is a property, not a method. The last index is always `length - 1`, so the last item is `fruits[fruits.length - 1]`, which is `"cherry"`. There is a shorter way too: the `at` method accepts a negative number and counts from the end, so `fruits.at(-1)` is `"cherry"`. An empty array has a `length` of `0`.

## push and pop at the back

Think of a train. You can hook a car on at the back, or take the last car off. `push` adds an item to the end and hands back the new length, so `fruits.push("date")` makes the list apple, banana, cherry, date and gives `4`. `pop` removes the last item and hands it back to you, so `const last = fruits.pop()` gives `"date"` and the array goes back to three items. `pop` on an empty array is safe: it just gives you `undefined`. These two are the workhorses, and they are quick because nothing else has to move.

## unshift and shift at the front

`unshift` adds an item to the start: `fruits.unshift("fig")` puts `"fig"` at index 0 and everything else slides one place along. `shift` removes the first item and hands it back, the mirror of `pop`. One honest warning: because every item has to slide along, `unshift` and `shift` get slower on a very long list. For a few items you will never notice. Remember it this way: `push` and `pop` work at the back, `unshift` and `shift` work at the front.

## splice: edit the middle

Sometimes you want to edit the middle, like fixing a playlist. That is `splice`. It takes a start index, how many items to remove, and then anything you want to put in. Start with `[10, 20, 30, 40, 50]`. `nums.splice(1, 2)` starts at index 1 and removes two items, so 20 and 30 are gone and you are left with `[10, 40, 50]`. To insert without removing anything, say zero items to remove: `nums.splice(1, 0, 99, 98)` puts 99 and 98 in at index 1 and nothing is lost. `splice` changes the original array, and hands back the removed items in a new one.

## slice: copy part of an array

`slice` sounds the same but is very different. It cuts a copy and leaves the original alone, like photocopying a few pages out of a book. `nums.slice(1, 4)` gives the items from index 1 up to, but not including, index 4. Leave out the second number and you get everything from there to the end, `slice()` with no numbers makes a full copy, and a negative number counts from the end, so `slice(-2)` gives the last two. An easy way to remember it: `slice`, with an i, is a copy. `splice`, with a p, pokes the original.

## Copying arrays: alias or spread

Now the surprise. `const alias = nums` is not a copy. An array is not copied when you assign it: both names point to the very same list, like handing someone your house key instead of building them a new house. So after `alias.push(7)`, `nums` has the 7 too. To get a real, separate copy, use the spread, three dots inside square brackets: `const copy = [...nums]`. Now `copy` is its own list. `slice()` with no numbers does the same job. (Both make a shallow copy: if the array holds other arrays, those inner arrays are still shared.)

## includes and indexOf

Searching is like looking for a name on a guest list. `includes` asks whether something is in the list: `colors.includes("green")` is `true` and `colors.includes("pink")` is `false`. `indexOf` asks where it is: `colors.indexOf("blue")` is `2`, and if the item is not there you get `-1`. That `-1` is easy to mix up with a real index, so use `includes` when you only need a yes or no, and `indexOf` when you need the position. Both compare with triple equals, so the text has to match exactly.

## Array destructuring

Say you have `["x", "y", "z", "w"]` and want the first two as separate variables. Write `const [a, b] = list`. That is destructuring: it unpacks the list into labelled shelves, by position, so `a` gets `"x"` and `b` gets `"y"`. Add `...others` at the end, as in `const [a, b, ...others] = list`, and `others` collects the rest into a new array, `["z", "w"]`. If the array is too short, the missing ones are `undefined`, but you can give a default, like `const [only = "none"] = []`, which gives `"none"`. And a neat trick: swap two variables with `[a, b] = [b, a]`.

## Why a const array can still change

`const` means the name always points to the same list. It does not freeze the list. So after `const pinned = ["a"]`, `pinned.push("b")` works fine and `pinned` is `["a", "b"]`. What `const` stops is pointing the name at a different list: `pinned = []` is a `TypeError`. It is the same idea as the alias: the name is the key, and the key never changes, but what is in the house can. Use `const` for arrays by default and you can still add and remove items.

## Common mistakes

1. Counting from one. The first item is at index 0, and the last is at `length - 1`.
2. Thinking equals makes a copy. Use `[...nums]` or `nums.slice()`.
3. Mixing up `slice` and `splice`. One copies, the other changes the original.
4. Using `indexOf` in an `if`. `-1` counts as true and `0` counts as false, so it breaks. Use `includes`.
5. Expecting an error for a missing index. You get `undefined`.

## The code, line by line

The first program covers the basics:

```javascript
const fruits = ["apple", "banana", "cherry"];
console.log(fruits[0]);
console.log(fruits[fruits.length - 1]);
console.log(fruits[5]);

fruits.push("date");
fruits.unshift("fig");
console.log(fruits);

const last = fruits.pop();
const first = fruits.shift();
console.log(last, first, fruits);
```

```output
apple
cherry
undefined
[ 'fig', 'apple', 'banana', 'cherry', 'date' ]
date fig [ 'apple', 'banana', 'cherry' ]
```

Line 3 reads the last item with `length - 1`, and line 4 asks for index 5 and prints `undefined`. Lines 6 and 7 add `"date"` at the back and `"fig"` at the front. Lines 10 and 11 take one off each end.

The second program covers cutting and copying:

```javascript
const nums = [10, 20, 30, 40, 50];
const middle = nums.slice(1, 4);
console.log(middle, nums);

nums.splice(1, 2);
console.log(nums);

nums.splice(1, 0, 99, 98);
console.log(nums);

const alias = nums;
const copy = [...nums];
alias.push(7);
console.log(nums.length, copy.length);
```

```output
[ 20, 30, 40 ] [ 10, 20, 30, 40, 50 ]
[ 10, 40, 50 ]
[ 10, 99, 98, 40, 50 ]
6 5
```

The slice is a copy and `nums` is untouched. After the splice, `nums` shrinks, then the insert grows it again. The last line prints `6 5`: pushing through `alias` changed `nums`, but `copy` stayed at five.

The third program covers searching and unpacking:

```javascript
const colors = ["red", "green", "blue"];
console.log(colors.includes("green"));
console.log(colors.indexOf("blue"));
console.log(colors.indexOf("pink"));

const [a, b, ...others] = ["x", "y", "z", "w"];
console.log(a, b, others);

const list = [];
console.log(list[0], list.length);
const [only = "none"] = list;
console.log(only);

const pinned = ["a"];
pinned.push("b");
console.log(pinned);
```

```output
true
2
-1
x y [ 'z', 'w' ]
undefined 0
none
[ 'a', 'b' ]
```

## What you learned

- An array is an ordered list in square brackets, and the index starts at 0.
- `length` is how many items there are, and the last item is at `length - 1`.
- `push` and `pop` work at the back, `unshift` and `shift` work at the front.
- `splice` edits the original array, and `slice` makes a copy.
- Equals does not copy an array, the spread `[...nums]` does.
- `includes` says yes or no, and `indexOf` says where, or `-1`.
- Destructuring unpacks a list into variables.
- `const` stops the name from changing, not the list.

## Common questions

**How do I check whether an array is empty?** Check its length: `list.length === 0`. An empty array is still truthy in an `if`, so `if (list)` does not work for this.

**How do I empty an array?** Set `list.length = 0`, or point a `let` variable at a new `[]`. Setting the length to zero empties the same list, so every name that points at it sees the change.

**Does `[...nums]` copy arrays inside arrays?** No. Spread and `slice` make a shallow copy. For `[[1], [2]]`, the outer list is new, but the inner lists are still shared, so pushing onto an inner one shows up in both.

**Why does `indexOf` give `-1`?** It means the item was not found. Because `-1` is easy to mistake for a real position, use `includes` when you only need to know whether something is there.

**Can an array hold different types?** Yes. `["hi", 42, [1, 2]]` is a valid array with a string, a number and another array.

Next in the series: array methods, where you loop over lists and turn them into new ones.
