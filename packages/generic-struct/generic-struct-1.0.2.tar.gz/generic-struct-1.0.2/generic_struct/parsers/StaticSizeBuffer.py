from generic_struct.parsers import Parser, validated_parser, ParserError


class StaticSizeBufferOversizeBufferError(ParserError):
    pass

@validated_parser
class StaticSizeBufferParser(Parser):
    _TYPES = str,

    def __init__(self, size):
        self._size = size

    def generate_buffer(self, value):
        if len(value) > self._size:
            raise StaticSizeBufferOversizeBufferError('cannot process buffer larger than {}, '
                                                      'length was {}'.format(self._size, len(value)))
        # fill buffer up to desired size
        while len(value) < self._size:
            value += '\x00'

        return value.encode()

    def calc_size(self, value):
        return self._size

    def parse(self, buffer):
        return buffer[:self._size].decode()
