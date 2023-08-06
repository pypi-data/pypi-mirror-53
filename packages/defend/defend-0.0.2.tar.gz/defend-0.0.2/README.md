# defend

`pip install defend`

#### usage
```python
from defend import debug
import os, time

os.environ['DEBUG'] = '*'

# ---

@debug('world', expect='world', istype=str, time_limit=2)
def say_hello(val):
  time.sleep(1)
  print(val)
  return val

@debug(expect=True)
def true_or_die(val):
  if not val: raise Exception('not val')
  else: return True

@debug(istype=int, verbose=True, active=True)
def math_func(a, b):
  return a + b
  
@debug(9, 6, istype=str, verbose=True, active=True)
def math_func_failed(a, b):
  return a + b

# ---

say_hello('hello')
true_or_die(True)
math_func(1,2)
math_func_failed(1,2)
```

#### output
<img src="https://github.com/selfquery/defend/blob/master/docs/result.png" />