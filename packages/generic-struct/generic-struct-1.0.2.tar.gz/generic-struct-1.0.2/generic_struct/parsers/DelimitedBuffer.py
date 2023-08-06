from generic_struct.parsers import Parser, validated_parser


@validated_parser
class DelimitedBufferParser(Parser):
    """
    a parser for a buffer with a delimiter
    """
    _TYPES = str,

    def __init__(self, delimiter=b'\x00'):
        """
        :param delimiter: a binary string which determines the end of the buffer
        :type delimiter: C{bytes}
        """
        self._delimiter = delimiter

    def generate_buffer(self, value):
        return value.encode() + self._delimiter

    def calc_size(self, value):
        return len(value) + len(self._delimiter)

    def parse(self, buffer):
        size = buffer.index(self._delimiter)
        return buffer[:size].decode()
