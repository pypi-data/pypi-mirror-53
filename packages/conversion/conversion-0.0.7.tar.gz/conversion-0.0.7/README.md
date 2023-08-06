# conversion

Utility functions to convert strings to Python types.


## convert_base64

Converts base64 encoded strings or bytes into strings:

```
>>> from conversion import convert_base64
>>> convert_base64('dGVzdA==')
'test'
```

If the payload is expected to be bytes, string conversion can be suppressed:

```
>>> convert_base64('dGVzdA==', convert_string=False)
b'test'
```

When the function does not find the string can be converted, an exception can be raised:

```
>>> convert_base64('dGVzdA=', raise_exceptions=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/berto/Projects/home/conversion/conversion/base64.py", line 28, in convert_base64
    converted = base64.b64decode(value)
  File "/Users/berto/.local/share/virtualenvs/conversion-bncB6LgQ/lib/python3.6/base64.py", line 87, in b64decode
    return binascii.a2b_base64(s)
binascii.Error: Incorrect padding
```


## convert_bool

Converts truthy strings to `True` and falsey strings to `False`:

```
>>> from conversion import convert_bool
>>> convert_bool('yes')
True
>>> convert_bool('no')
False
```

When the function does not find the string can be converted, ValueError is
raised:

```
>>> convert_bool('yup')
ValueError: invalid truth value 'yup'
```


## convert_delta

Converts time with unit suffixes into `datetime.timedelta` objects:

```
>>> from conversion import convert_delta
>>> convert_delta('1h')
datetime.timedelta(0, 3600)
```


## convert_json

Converts JSON strings into objects:

```
>>> from conversion import convert_json
>>> convert_json('{"some": "dict", "in": "json"}')
{'some': 'dict', 'in': 'json'}
```


## convert_list

Converts a comma-delimited string into a list:

```
>>> from conversion import convert_list
>>> convert_list('a,comma,delimited,list')
['a', 'comma', 'delimited', 'list']
```

And an optional kwarg can specify the delimiter:

```
>>> convert_list('a:colon:delimited:list', delimiter=':')
['a', 'colon', 'delimited', 'list']
```
