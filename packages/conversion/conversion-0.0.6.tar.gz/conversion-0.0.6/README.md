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
>>> from conversion import convert_list
>>> convert_list('a:colon:delimited:list', delimiter=':')
['a', 'colon', 'delimited', 'list']
```
