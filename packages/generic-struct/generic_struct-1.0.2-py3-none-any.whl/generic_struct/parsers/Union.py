from generic_struct.parsers import Parser, validated_parser, ParserError
from generic_struct.structs import Struct


class UnionCannotFindParserError(ParserError):
    pass


@validated_parser
class UnionParser(Parser):
    _TYPES = object,

    def __init__(self, type_enum_parser, type_parsers):
        self._type_enum_parser = type_enum_parser
        self._type_parsers = type_parsers

    def generate_buffer(self, value):
        idx = self.__pick_parser(value)
        return self._type_enum_parser.generate_buffer(idx) + self._type_parsers[idx].generate_buffer(value)

    def calc_size(self, value):
        idx = self.__pick_parser(value)
        return self._type_enum_parser.calc_size(idx) + self._type_parsers[idx].calc_size(value)

    def parse(self, buffer):
        parser_idx = self._type_enum_parser.parse(buffer)
        return self._type_parsers[parser_idx].parse(buffer[self._type_enum_parser.calc_size(parser_idx):])

    def __pick_parser(self, value):
        """
        find the index of the proper parser for a given object
        :param value:
        :return: The value's corresponding parser
        :rtype: C{Parser}
        """

        possible_parsers = []
        for parser in self._type_parsers:
            try:
                parser.generate_buffer(value)
            except Exception:
                continue
            possible_parsers.append(parser)

        possible_parsers = [parser for parser in self._type_parsers if any(isinstance(value, field_type)
                                                                           for field_type in parser._TYPES)]

        if len(possible_parsers) == 1:
            parser = possible_parsers[0]
        elif isinstance(value, Struct):
            parser = [parser for parser in possible_parsers if type(value) in parser._TYPES][0]
        elif len(possible_parsers) == 0:
            raise UnionCannotFindParserError("could not find parser for data type {}".format(type(value)))
        else:
            possible_parsers = [parser for parser in possible_parsers if type(value) in parser._TYPES]
            if len(possible_parsers) == 1:
                parser = possible_parsers[0]
            else:
                raise UnionCannotFindParserError("too many parser possibilities for type{}."
                                                 " possible parsers: {}".format(type(value), possible_parsers))

        return self._type_parsers.index(parser)
