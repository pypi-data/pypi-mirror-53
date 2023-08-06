# wai-common
Python library with common functionality for other Waikato projects.

## Sub-modules

### abc
Functions for working with abstract classes and methods.

---
### decorator
Custom decorators.

---
### file
Classes and readers for common file types. Currently supports ARFF, CSV and spec files.

---
### iterate
Utility functions for working with iterators and iterables.

---
### sequence
Utility functions for working with sequences.

---
### memoise
Provides memoisation of function calls, so that long-running functions can restore
their results from disk instead of repeated calling.

Usage:
```python
from wai.common import MemoiserFactory

def my_long_running_function(*args, **kwargs):
    ...

factory = MemoiserFactory("./memo_fib/")
my_memo_function = factory(my_long_running_function)

args, kwargs = ...
result1 = my_memo_function(*args, **kwargs)
result2 = my_memo_function(*args, **kwargs)  # Second call loads result from disk

assert result1 == result2

```
---
### pool
Utility functions for working with `multiprocessing.Pool` objects. Provides:
* **num_processes**: Gets the number of sub-processes managed by the pool (normally
                     a protected member).
* **run_on_all**: Runs the given function on all sub-processes managed by a pool.

---
### switch
The switch module provides a switch/case-like pattern for operating with enumerate
values.

Usage:
```python
from wai.common import switch, case, default, break_

x: MyEnum = ...

with switch(x):
    # Standard case-block
    if case(MyEnum.ENUM_1):
        ...
        break_()
        
    # Case-block with fall-through
    if case(MyEnum.ENUM_2):
        ...
    if case(MyEnum.ENUM_3):
        ...
        break_()
        
    # Multi-case
    if case(MyEnum.ENUM_4, MyEnum.ENUM_5):
        ...
        break_()
        
    # Default block (only executes if no other case matched)
    if default():
        ...
```
---
### TwoWayDict
Provides the TwoWayDict class, a dictionary which can be accessed by key or by value.

```python
from wai.common import TwoWayDict

twd = TwoWayDict[str, int]()
twd['one'] = 1
twd[2] = 'two'
twd['three'] = 3

print(twd[1])  # 'one'

```

---
### onehot
Helper classes for performing one-hot encoding of nominal data.

---