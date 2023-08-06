from generic_struct.parsers import Parser, validated_parser, ParserError


class StaticSizeListBadSizeError(ParserError):
    pass


@validated_parser
class StaticSizeListParser(Parser):
    _TYPES = list,

    def __init__(self, element_parser, size):
        self._element_parser = element_parser
        self._size = size

    def generate_buffer(self, value):
        if len(value) != self._size:
            raise StaticSizeListBadSizeError('got {} elements! expected {}'.format(len(value), self._size))
        result = b''
        for item in value:
            result += self._element_parser.generate_buffer(item)
        return result

    def calc_size(self, value):
        if len(value) != self._size:
            raise StaticSizeListBadSizeError('got {} elements! expected {}'.format(len(value), self._size))
        return sum(self._element_parser.calc_size(item) for item in value)

    def parse(self, buffer):
        idx = 0
        result = []
        for i in range(self._size):
            result.append(self._element_parser.parse(buffer[idx:]))
            idx += self._element_parser.calc_size(result[-1])
        return result
