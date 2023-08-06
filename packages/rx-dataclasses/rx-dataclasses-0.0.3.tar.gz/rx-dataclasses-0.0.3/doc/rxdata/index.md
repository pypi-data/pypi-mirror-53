Module rxdata
=============
reactive dataclasses

Sub-modules
-----------
* rxdata.typeguard

Functions
---------

    
`dataclass(*, subject=None, rx=RXDataclassSettings(init=True, setattr=True, delattr=False), init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)`
:   During execution of this function - patch with own version of functions
    [dataclasses._field_assign, __setattr__, __delattr__].
    That versions of (dataclasses._field_assign, __setattr__, __delattr__) are specific for `_cls`
    class and contains its as closure.

    
`field(observe=[], pipeline=[], invoke=[], scheduler=None, rx=Field.RX(init=None, setattr=None, delattr=None), default=<dataclasses._MISSING_TYPE object at 0x7fb967eaaf90>, default_factory=<dataclasses._MISSING_TYPE object at 0x7fb967eaaf90>, init=True, repr=True, hash=None, compare=True, metadata=None)`
: