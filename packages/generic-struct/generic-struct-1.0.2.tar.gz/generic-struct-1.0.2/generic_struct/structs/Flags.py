from generic_struct.structs import Struct


class ReservedBitType(object):
    def __int__(self):
        return 0


RESERVED = ReservedBitType()


class ReservedBits(object):
    def __init__(self, size=1):
        self.size = size

    def generate_padding(self):
        return tuple([RESERVED] * self.size)


def flags(*fields):
    """
    create a bitfield buffer
    :param fields: names of the bits in the bitfields
    :rtype: C{type}
    """
    while any(isinstance(field_name, ReservedBits) for field_name in fields):
        idx = [type(field_name) for field_name in fields].index(ReservedBits)
        fields = fields[:idx] + fields[idx].generate_padding() + fields[idx + 1:]

    while len(fields) % 8 != 0:
        fields += RESERVED,

    class Flags(Struct):
        def __init__(self, *args, **kwargs):
            for field_name in fields:
                if field_name != RESERVED:
                    self.__setattr__(field_name, None)

            for i, value in enumerate(args):
                self.__setattr__([name for name in fields if name != RESERVED][i], value)

            for name, value in kwargs.items():
                self.__setattr__(name, value)

        def get_buffer(self):
            bits = ''
            for field_name in fields:
                if type(field_name) == str:
                    bits += str(int(self.__getattribute__(field_name)))
                else:
                    bits += '0'
            return bytes(int(bits[i:][:8], base=2) for i in range(0, len(bits), 8))

        def read_buffer(self, buffer):
            bits = [bool(int(bit)) for byte in buffer for bit in bin(byte)[2:].zfill(8)]
            used_bits = [bit for i, bit in enumerate(bits) if type(fields[i]) == str]
            for i, value in enumerate(used_bits):
                self.__setattr__([name for name in fields if name != RESERVED][i], value)

        @staticmethod
        def get_buffer_size(**kwargs):
            return len(fields) / 8

        def __iter__(self):
            return ((key, self.__getattribute__(key)) for key in fields if type(key) is str)

    return Flags


def build_flags(fields_class):
    return flags(*fields_class().FIELDS)
