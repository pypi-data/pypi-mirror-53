# Magic Results

Usage:

```
# -*- coding: macro -*-

from magicresult import Result, ok, error, attempt

def get_str_ok() -> Result[str]:
    return ok("hello world")

def get_str_err() -> Result[str]:
    return error("something went wrong")

def magic_example() -> Result[None]:
    a = attempt(get_str_ok())
    print("First string is: " + a)
    b = attempt(get_str_err())
    print("Second string is: " + b)
    return ok(None)

print(f"magic_example returned {magic_example()}")
```