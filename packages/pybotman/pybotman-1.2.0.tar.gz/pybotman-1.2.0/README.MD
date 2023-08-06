# PyBotman
#### Python Botman API Wrapper
Written by Flowelcat

Introduction
---
This library provides a pure Python interface for the Botman API. It works with Python 3+.

Botman API provides bot control features along with providing some methods for fetching data from bot's database.

Installing
---
You can install pybotman using:

```console
$ pip install pybotman
```

Using
---
```python
from pybotman import BotmanApi

botman = BotmanApi("https://example.com/v1/", "some_token")
print(botman.get_api_status())
```