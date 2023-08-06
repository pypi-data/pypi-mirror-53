# conversion

Utility functions to convert strings to Python types.


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
