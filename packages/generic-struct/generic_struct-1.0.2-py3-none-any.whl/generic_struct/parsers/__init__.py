class ParserError(Exception):
    pass


class Parser(object):
    """
    a generic parser
    """
    _TYPES = object,

    def generate_buffer(self, value):
        """
        generate a buffer from a given value
        :param value: an object that can be parsed using this class
        :rtype: C{bytes}
        """
        raise NotImplementedError()

    def calc_size(self, value):
        """
        calculate the size of the buffer generated from a given value
        :param value: an object that can be parsed using this class
        :rtype: C{int}
        """
        raise NotImplementedError()

    def parse(self, buffer):
        """
        parse a binary buffer into an object
        :return: the parsed object
        """
        raise NotImplementedError()


class StructParser(Parser):
    """
    a parser for classes derived from generic_struct.structs.Struct
    """

    def __init__(self, struct_type):
        self._TYPES = struct_type,
        self._type = struct_type

    def generate_buffer(self, value):
        return value.get_buffer()

    def calc_size(self, value):
        return value.get_buffer_size()

    def parse(self, buffer):
        result = self._type()
        result.read_buffer(buffer)
        return result


def validate_arguments(**type_matches):
    for key, value in type_matches.items():
        try:
            iter(value)
        except TypeError:
            type_matches[key] = value,

    def validate_inner(func):
        def validated_func(*args, **kwargs):
            for name, value in kwargs.items():
                if not name in type_matches.keys():
                    continue
                if all(not isinstance(value, arg_type) for arg_type in type_matches[name]):
                    raise TypeError("the argument '{}' must be of the types {}".format(name, type_matches[name]))
            for idx, value in enumerate(args):
                name = func.__code__.co_varnames[idx]
                if all(not isinstance(value, arg_type) for arg_type in type_matches[name]):
                    raise TypeError("the argument '{}' must be of the types {}, given value is {}".format(name, type_matches[name], value))

            return func(*args, **kwargs)

        return validated_func

    return validate_inner


def validated_parser(parser_class):
    class ValidatedParser(parser_class):
        @validate_arguments(self=object, value=parser_class._TYPES)
        def generate_buffer(self, value):
            return super().generate_buffer(value)

        @validate_arguments(self=object, value=parser_class._TYPES)
        def calc_size(self, value):
            return super().calc_size(value)

    return ValidatedParser
