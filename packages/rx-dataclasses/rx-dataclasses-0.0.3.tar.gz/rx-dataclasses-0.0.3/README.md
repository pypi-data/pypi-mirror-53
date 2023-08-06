## rx-dataclasses

### type verification and convert

```python
from typing import *
from rx.operators import map as rxmap
from rxdata import dataclass, field, operators

@rxmap
def try_convert(n):
    return int(n) if isinstance(n, str) and n.isalpha() else n

@dataclass
class Data:
    # only int.
    number: int                         = field(default=1,
                                                invoke=operators.typeguard())

    # only int or string convertable to int. Always results in int.
    convert_or_die: Union[int]          = field(default=1,
                                                invoke=[try_convert,
                                                        operators.typeguard()])

    # If is string and convertable to int - perform conversion. `typing.Any` type defined explicitly during `invoke` (just for example).
    convert_or_accept: Union[int, str]  = field(default=1,
                                                invoke=[try_convert,
                                                        operators.typeguard(Any)])


> data = Data(None)
TypeError: type of number must be int; got NoneType instead

> data = Data(convert_or_die=None)
TypeError: type of convert_or_die must be int; got NoneType instead

> Data(convert_or_accept=None)
Data(number=1, convert_or_die=1, convert_or_accept=None)


data = Data()

data.number = '3'
> TypeError: type of number must be int; got str instead

data.number = 2
> Data(number=2, convert_or_die=1, convert_or_accept=1)

data.convert_or_die = 2
> Data(number=2, convert_or_die=2, convert_or_accept=1)

data.convert_or_accept = '3'
> Data(number=2, convert_or_die=2, convert_or_accept=3)

data.convert_or_accept = '3s'
> Data(number=2, convert_or_die=2, convert_or_accept='3s')

data.convert_or_accept = type
> Data(number=2, convert_or_die=2, convert_or_accept=<class 'type'>)
```


## description

reactive python3 dataclasses - with `attrs`-like behaviour

* implicit and explicit typing verification during both `init` and/or `setattr`
* customize preprocessing (convert) during both `init` and/or `setattr`
* reactive attributes

## install

```
> pip3 install rx-dataclasses
```
