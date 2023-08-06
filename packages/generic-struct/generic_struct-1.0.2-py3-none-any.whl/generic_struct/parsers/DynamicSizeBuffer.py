from generic_struct.parsers import Parser, validated_parser


@validated_parser
class DynamicSizeBufferParser(Parser):
    """
    a parser for a buffer with its size written before the buffer
    """

    _TYPES = str,

    def __init__(self, size_field_parser):
        """
        :param size_field_parser: a parser for the buffer size field
        :type size_field_parser: C{Parser}
        """
        self._size_field_parser = size_field_parser

    def generate_buffer(self, value):
        result = self._size_field_parser.generate_buffer(len(value))
        result += value.encode()
        return result

    def calc_size(self, value):
        return len(value) + self._size_field_parser.calc_size(len(value))

    def parse(self, buffer):
        size = self._size_field_parser.parse(buffer)
        result = buffer[self._size_field_parser.calc_size(size):][:size].decode()
        return result
