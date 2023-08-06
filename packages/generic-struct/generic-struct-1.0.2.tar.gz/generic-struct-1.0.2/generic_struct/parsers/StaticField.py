import struct

from generic_struct.parsers import Parser, validated_parser


class StaticFieldParser(Parser):
    """
    a parser for the basic python types, uses the struct module
    """
    _TYPES = int, float, bytes, bool

    def __init__(self, format):
        """
        :param format: format to pass to struct.pack and struct.unpack_from
        :type format: C{str}
        """
        self._format = format

    def generate_buffer(self, value):
        return struct.pack(self._format, value)

    def calc_size(self, value):
        return struct.calcsize(self._format)

    def parse(self, buffer):
        result, = struct.unpack_from(self._format, buffer)
        return result


class UnsignedIntFormats(object):
    BYTE = '>B'
    BE_WORD = '>H'
    BE_DWORD = '>L'
    BE_QWORD = '>Q'
    LE_WORD = '<H'
    LE_DWORD = '<L'
    LE_QWORD = '<Q'

    ALL = (BYTE, BE_WORD, BE_DWORD, BE_QWORD, LE_WORD, LE_DWORD, LE_QWORD)


class SignedIntFormats(object):
    BYTE = '>b'
    BE_WORD = '>h'
    BE_DWORD = '>l'
    BE_QWORD = '>q'
    LE_WORD = '<h'
    LE_DWORD = '<l'
    LE_QWORD = '<q'

    ALL = (BYTE, BE_WORD, BE_DWORD, BE_QWORD, LE_WORD, LE_DWORD, LE_QWORD)


class FloatFormats(object):
    BE_DWORD = '>f'
    BE_QWORD = '>d'
    LE_DWORD = '<f'
    LE_QWORD = '<d'

    ALL = (BE_DWORD, BE_QWORD, LE_DWORD, LE_QWORD)


BOOL_FORMAT = '<?'
CHAR_FORMAT = '<c'
