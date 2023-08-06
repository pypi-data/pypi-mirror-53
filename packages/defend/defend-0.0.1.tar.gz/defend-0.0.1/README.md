# defend

```python
from defend import debug
import os, time

os.environ['DEBUG'] = '*'

@debug('world', expect='world', istype=str, time_limit=2, verbose=True)
def say_hello(val):
  time.sleep(1)
  return val

@debug(expect=True, verbose=True)
def true_or_die(val):
  if not val: raise Exception('not val')
  else: return True

@debug(istype=int, verbose=True, active=True)
def math_func(a, b):
  return a + b

say_hello('hello')
```