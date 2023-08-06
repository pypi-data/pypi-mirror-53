This package allows quick and simple creation of protocol-handling classes. It consists of two maintypes -
`Struct` and `Parser` - where `Struct` represent an object with fields and a `Parser` is used to parse said
fields from and into binary buffers; the package also includes some basic `Parser`s and `Struct`s which can
be dynamically built to fit the developer's needs.

# Usage

## Structs

The class `generic_struct.structs.Struct` is the basic protocol-handling class. it has members to represent the
different fields in the protocol and the API to write buffers from its fields and read its fields from buffers.
All protocol-handling classes created using `generic_struct` are derived from `Struct`.

The methods of `Struct`:
* `get_buffer()` - create a binary buffer (a `bytes` object) representing the current fields of the struct
* `read_buffer(buffer)` - read a binary buffer into the fields of the struct
* `get_buffer_size()` - get the length of the corresponding binary buffer


### How to create a `Struct` class

The current version includes two types of `Struct`s which can be created  

#### generic_struct.structs.GenericStruct

This type of `Struct` has fields of varying types and generates buffers using each field's 
corresponding `Parser`.

To create a `Struct` of that type you can use the class-decorator `generic_struct.structs.GenericStruct.build_struct`:
```python
from generic_struct.structs.GenericStruct import build_struct

@build_struct
class MyStruct():
    <field_name> = <field_parser>
    <field_name> = <field_parser>   
    ...
```

object of this type of `Struct` can be converted to `dict`


#### generic_struct.structs.Flags

This type of `Struct` handles flags fields. Each field is a `bool` object and has a designated
bit in the serialized buffer. 

A `Struct` of this type is created usnig the class-decorator `generic_struct.structs.Flags.build_flags`:

```python
from generic_struct.structs.Flags import build_flags

@build_flags
class MyFlags():
    FIELDS = ['list', 'of', 'field', 'names']
```

Where The first element in the FIELDS list is the most significant bit of the first byte in the buffer, and so on.

To have more control over the positions of the bits in the buffer, you can insert
`generic_struct.structs.Flags.RESERVED` to represent one unused bit or `generic_struct.structs.Flags.ReservedBits(n)`
to represent `n` unused bits. unused bits in the buffer are Always 0. 

```python
from generic_struct.structs.Flags import build_flags, RESERVED, ReservedBits

@build_flags
class MyFlags():
    FIELDS = [ReservedBits(5), 'some', 'bits', 'are', RESERVED , 'bits']
```

object of this type of `Struct` can be converted to `dict`

## Parsers
A `Parser` class is responsible to converting between a specific `type` and a binary buffer in a specific way;
_converting between `int` and an unsigned big-endian 4-bytes integer, for example._

`Parser`s are mainly used in the creation of `Struct` classes.

The more complicated `Parser`s use other `Parser`s in order to do their work. 

This package contains a bunch of common useful `Parser`s:

|Parser |Supported Types |Buffer type    |
|------ |------          |-----------    |
|generic_struct.parsers.StaticField.StaticFieldParser|`int`, `bool`, `float`, `bytes`|simple conversion using the `struct` module|
|generic_struct.parsers.StaticSizeBuffer.StaticSizeBufferParser|`str`|a buffer with a pre-determined size|
|generic_struct.parsers.DynamicSizeBuffer.DynamicSizeBufferParser|`str`|length of the buffer, then the buffer|
|generic_struct.parsers.StaticSizeList.StaticSizeListParser|`list`|every element of a pre-defined size list, parsed with a `Parser` for the elements|
|generic_struct.parsers.DynamicSizeList.DynamicSizeListParser|`list`|length of the list, then the elements of the list|
|generic_struct.parsers.DelimitedBuffer.DelimitedBufferParser|`str`|a buffer with a delimiter buffer/byte at its end|
|generic_struct.parsers.DelimitedList.DelimitedListParser|`str`|a list with a delimiter object at its end|
|generic_struct.parsers.StructParser|`Struct`|a parser for a specific type of `Struct`|
|generic_struct.parsers.Union.UnionParser|any one of a list of `Struct`s|a number which defines the parsed type, then the parsed object|

### generic_struct.parsers.StaticField.StaticFieldParser
The most simple `Parser` is ``. This `Parser` wraps the
functionality of `struct.pack()` and `struct.unpack_from()`, although meant to handle mainly `int` and `float`.

The `generic_struct.parsers.StaticField` module also contains wrappers for the different types `StaticFieldParser`
can handle: `SignedIntFormats`, `UnsignedIntFormats`, `FloatFormats`, `CHAR_FORMAT`, and `BOOL_FORMAT`. 

_Example_: The parser `StaticFieldParser(SignedIntFormats.BE_DWORD)` would serialize `11` as `b'\x00\x00\x00\x11'`

### generic_struct.parsers.StaticSizeBuffer.StaticSizeBufferParser
This parser packs a `str` into a buffer of a static size. Too short strings are padded with `b'\x00'`.
For example, the string `'some txt'` will be converted to `b'some txt\x00\x00'`.

**Note**: trailing `b'\x00'`s are not automatically removed by `StaticSizeBufferParser.parse()`. The buffer 
`b'some txt\x00\x00'` is parsed as the string `'some txt\x00\x00'`. 

### generic_struct.parsers.DynamicSizeBuffer.DynamicSizeBufferParser

This parser packs a `str` into a dynamic sized buffer. The buffer begins with the length of the string, serialized
by a `Parser` that can serialize the type `int`, and then the string itself.

_Example_: the parser `DynamicSizeBufferParser(StaticFieldParser(UnsignedIntFormats.BYTE))` serializes the string
`'some string'` as the buffer `b'\x0bsome string'`, while the parser
`DynamicSizeBufferParser(StaticFieldParser(UnsignedIntFormats.LE_DWORD))` serializes it as
`b'\x0b\x00\x00\x00some string'` 

### generic_struct.parsers.StaticSizeList.StaticSizeListParser

This parser packs a static-sized `list` into a buffer, with the elements packed by a `Parser`
that can parse all the elements in the list.

_Example_: the parser `StaticSizeListParser(element_parser=StaticFieldParser(SignedIntFormats.LE_WORD), size=3)`
serializes the list `[3,-1,5]` as `b'\x03\x00\xff\xff\x05\x00'`

### generic_struct.parsers.DynamicSizeList.DynamicSizeListParser

This parser packs a dynamic-sized list into a buffer similarly to
`generic_struct.parsers.StaticSizeList.StaticSizeListParser`, except that the size of the list is added at the beginning
of the buffer

_Example_: the parser
```
DynamicSizeListParser(element_parser=StaticFieldParser(SignedIntFormats.LE_WORD),
                      size_parser=StaticFieldParser(SignedIntFormats.BYTE))
```
serializes the list `[3,-1,5]` as `b'\x03\x03\x00\xff\xff\x05\x00'`

### generic_struct.parsers.DelimitedBuffer.DelimitedBufferParser

This parser packs a string as a buffer with a delimiter. The delimiter is a `bytes` of any length

_Example_: the parser `DelimitedBufferParser(b'\x93)` serializes the string `'some_string'` as `b'some_string\x93'`

### generic_struct.parsers.DelimitedList.DelimitedListParser

This parser packs a `list` as a buffer with a delimiter: The elements packed by a `Parser`
that can parse all the elements in the list, and then a delimiter with its own `Parser`

_Example_: the parser
```
DelimitedListParser(element_parser=StaticFieldParser(SignedIntFormats.LE_WORD),
                    delimiter=700,
                    delimiter_parser=StaticFieldParser(UnsignedIntFormats.BE_DWORD))
```
serializes the list `[3,-1,5]` as `b'\x03\x00\xff\xff\x05\x00\x00\x00\x02\xbc'`

### generic_struct.parsers.StructParser

This parser packs a child-class of `Struct`. it is useful when one wishes one of the fields in their `Struct` to be 
a `Struct`. 

### generic_struct.parsers.Union.UnionParser

This parser packs one of a list of types, and adds a type identifier field packed with its own parser
at the beginning of the buffer.

_Example_: The parser
```
UnionParser(type_enum_parser=StaticFieldParser(UnsignedIntFormats.BYTE),
            type_parsers=[StaticFieldParser(FloatFormats.BE_QWORD),
            DelimitedBufferParser(b'\x00')])
```

serializes:
* `124.34` as `b'\x00@_\x15\xc2\x8f\\(\xf6'`
* `'some string'` as `b'\x01some string\x00'`


## Example

```python
from generic_struct.parsers import StructParser
from generic_struct.parsers.DelimitedBuffer import DelimitedBufferParser
from generic_struct.parsers.DelimitedList import DelimitedListParser
from generic_struct.parsers.DynamicSizeBuffer import DynamicSizeBufferParser
from generic_struct.parsers.StaticField import StaticFieldParser, UnsignedIntFormats, CHAR_FORMAT
from generic_struct.parsers.StaticSizeList import StaticSizeListParser
from generic_struct.parsers.Union import UnionParser
from generic_struct.structs.Flags import ReservedBits, build_flags
from generic_struct.structs.GenericStruct import build_struct


@build_flags
class MyFlags(object):
    FIELDS = [ReservedBits(5), 'bool_a', 'bool_b', 'bool_c']


@build_struct
class MyStruct(object):
    word_int = StaticFieldParser(UnsignedIntFormats.BE_WORD)
    byte_int = DynamicSizeBufferParser(StaticFieldParser(UnsignedIntFormats.BYTE))
    delim_list = DelimitedListParser(element_parser=DelimitedBufferParser(b'::'),
                                     delimiter=b'$',
                                     delimiter_parser=StaticFieldParser(CHAR_FORMAT))
    union = UnionParser(StaticFieldParser(UnsignedIntFormats.BYTE),
                        [StructParser(MyFlags),
                         StaticSizeListParser(StaticFieldParser(UnsignedIntFormats.BE_DWORD), 4),
                         DelimitedBufferParser(b';')])


def main():
    struct1 = MyStruct(word_int=4,
                       byte_int='some_ string',
                       delim_list=['some', 'list', 'of', 'strings'],
                       union=MyFlags(bool_a=False, bool_b=False, bool_c=True))

    print('struct1:', dict(struct1))
    print('struct1.union:', dict(struct1.union))

    buffer1 = struct1.get_buffer()
    print('serialized:', buffer1)
    print()
    struct2 = MyStruct()
    struct2.read_buffer(buffer1)

    struct2.union = 'this is a string now'
    buffer2 = struct2.get_buffer()
    print('struct2:', dict(struct2))
    print('serialized:', buffer2)


if __name__ == '__main__':
    main()
```

the output would be:

```
struct1: {'word_int': 4, 'byte_int': 'some_ string', 'delim_list': ['some', 'list', 'of', 'strings'], 'union': <generic_struct.structs.Flags.flags.<locals>.Flags object at 0x03304810>}
struct1.union: {'bool_a': False, 'bool_b': False, 'bool_c': True}
serialized: b'\x00\x04\x0csome_ stringsome::list::of::strings::$\x00\x01'

struct2: {'word_int': 4, 'byte_int': 'some_ string', 'delim_list': ['some', 'list', 'of', 'strings'], 'union': 'this is a string now'}
serialized: b'\x00\x04\x0csome_ stringsome::list::of::strings::$\x02this is a string now;'
```