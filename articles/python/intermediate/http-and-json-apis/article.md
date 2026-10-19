title: Python HTTP and JSON APIs: fetch data with urllib
summary: How to call a web API in Python with only the standard library: send a request with urllib, turn the JSON response into a dictionary, and handle a bad address, a down network or a 404. One short script with its real output.
description: Python HTTP and JSON APIs explained: fetch data with urllib.request, turn the JSON into a dictionary with json.load, and catch URLError, with real output.
date: 2026-10-19
read: 5 min read
lesson: 15
video: Python HTTP and JSON APIs: Fetch Data with urllib | https://youtu.be/etiI3qWhWi0
image: cover.png
---
By the end of this page you will know how to fetch data from a web API in Python with nothing but the standard library, how to turn the JSON that comes back into a dictionary, and how to handle a request that fails. It builds on [Python files and JSON](/articles/python/beginner/files-and-json/), because the `json` module works the same way here, and on [Python errors and exceptions](/articles/python/beginner/errors-and-exceptions/).

## What is a web API in Python

A web API is a program you talk to with a web address. You send a request to a URL, and the server sends back a response. The response has a status code: 200 means it worked, and 404 means that address was not found. Inside the response is the data.

In our example the address is `https://jsonplaceholder.typicode.com/todos/1`, a free practice service that returns one to-do item.

## JSON becomes a dictionary

The data usually comes as JSON, which is just text. It looks like a dictionary, with keys and values. The `json` module turns that text into a real dictionary with `json.load`. After that, the title is one key lookup away, and so is the completed flag.

## When a request fails

Requests fail. The address can be wrong, or the network can be down. In Python, a failed request raises `urllib.error.URLError`. A 404 is a kind of `URLError` too: it raises `HTTPError`, which is a subclass of `URLError`. So one `except urllib.error.URLError` clause covers all of these, and the error's `reason` says what went wrong.

## The code

```python
import json
import urllib.error
import urllib.request

url = "https://jsonplaceholder.typicode.com/todos/1"
try:
    with urllib.request.urlopen(url, timeout=10) as response:
        todo = json.load(response)
    print(todo["title"])
    print(todo["completed"])
except urllib.error.URLError as error:
    print("failed:", error.reason)
```

```output
delectus aut autem
False
```

The output comes from a real server, so it needs an internet connection.

## The code line by line

- Lines 1 to 3 import `json` and the two `urllib` parts we need.
- Line 5 holds the address of one to-do item.
- Line 6 starts a `try`, because the request can fail.
- Line 7 opens the address with `urlopen`. The `timeout=10` gives up after ten seconds instead of waiting forever, and the `with` block closes the connection for us.
- Line 8 reads the response and turns the JSON into a dictionary.
- Lines 9 and 10 print two of its values.
- Line 11 catches a `URLError`.
- Line 12 prints the reason.

## What you learned

- A web API is a URL you send a request to. The response holds a status code and data.
- The data is usually JSON text, and `json.load` turns it into a dictionary.
- `urllib.request.urlopen(url, timeout=10)` inside a `with` block makes the request.
- `URLError` covers a bad address, a down network and a 404.
- `urllib` is built in, so it is enough for small jobs. For bigger ones, reach for `httpx`.

## Common questions

**What does the script print for an address that does not exist?** Change the URL to `https://jsonplaceholder.typicode.com/todos/99999` and it prints `failed: Not Found`. A made-up host name such as `nonexistent.invalid` prints something like `failed: [Errno 11001] getaddrinfo failed`, and the exact text depends on your system.

**How do I read the status code?** Inside the `with` block, `response.status` is the code, and it is `200` for a successful request. A 404 never gets that far, because `urlopen` raises `HTTPError` first, and its `code` attribute holds `404`.

**What if the server sends something that is not JSON?** `json.load` raises `json.JSONDecodeError`, with a message such as `Expecting value: line 1 column 1 (char 0)`. The script above does not catch it, because the example is a service that always sends JSON. Add `json.JSONDecodeError` to the `except` if you cannot trust the server.

**How do I send data instead of just fetching it?** `urlopen` takes a `urllib.request.Request` object, which can carry a method, headers and a body. It works, but it is wordy, and it is one of the reasons people move to `httpx` for bigger jobs.

**When should I use httpx?** `httpx` is a third-party library you install with `uv add httpx`. It has shorter code, a built-in `.json()` method on the response, and support for async. For one quick fetch in a script, `urllib` needs no install and is enough.

Next in the series: testing with pytest.
