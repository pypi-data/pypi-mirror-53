"""
Purpose :   A generic protocol-header class
Created :   13.09.2019
"""
from generic_struct.structs import Struct, StructError
from gc import get_referents


class GStructFieldDoesNotExistError(StructError):
    pass


def generic_struct(parent_class=None, **fields):
    """
    create a generic struct class that can create and read binary buffers
    :param parent_class: class to inherit from
    :type parent_class: C:{type}
    :param fields: the different fields in the struct
    :rtype fields: C{dict(C{str}:C{str})}
    :return: a class representing the desired struct
    :rtype: C{type}
    """
    parents = Struct,
    if not isinstance(parent_class, type):
        parents = Struct, parent_class,

    class GenericStruct(*parents):
        def __init__(self, *args, **kwargs):
            for name in kwargs.keys():
                if name not in fields.keys():
                    raise GStructFieldDoesNotExistError('no such field named {}'.format(name))
            for name, field_format in fields.items():
                self.__setattr__(name, None)

            for idx, value in enumerate(args):
                self.__setattr__(fields.keys()[idx], value)

            for name, value in kwargs.items():
                self.__setattr__(name, value)

        def get_buffer(self):
            result = b''
            for field, field_format in fields.items():
                result += field_format.generate_buffer(self.__getattribute__(field))
            return result

        def read_buffer(self, buffer):

            idx = 0
            for field, field_format in fields.items():
                self.__setattr__(field, field_format.parse(buffer[idx:]))
                idx += field_format.calc_size(self.__getattribute__(field))

        def get_buffer_size(self):
            return sum(parser.calc_size(self.__getattribute__(name)) for name, parser in fields.items())

        def __str__(self):
            return self.get_buffer().decode()

        def __iter__(self):
            return ((key, self.__getattribute__(key)) for key in fields.keys())

    return GenericStruct


def build_struct(fields_class):
    instance = fields_class()
    fields = {key : val for key, val in get_referents(fields_class)[0].items() if key[0] != '_'}
    return generic_struct(parent_class=fields_class, **fields)
