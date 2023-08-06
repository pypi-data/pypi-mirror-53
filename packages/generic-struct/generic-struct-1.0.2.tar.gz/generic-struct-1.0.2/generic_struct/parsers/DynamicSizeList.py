from generic_struct.parsers import Parser, validated_parser


@validated_parser
class DynamicSizeListParser(Parser):
    """
    a parser for a list with a size field at the begining
    """
    _TYPE = str

    def __init__(self, element_parser, size_parser):
        """
        :param element_parser: a parser for the elements in the list
        :type element_parser: C{Parser}
        :param size_parser: a parser for the list size field
        :type size_parser: C{Parser}
        """
        self._element_parser = element_parser
        self._size_parser = size_parser

    def generate_buffer(self, value):
        result = self._size_parser.generate_buffer(len(value))
        for item in value:
            result += self._element_parser.generate_buffer(item)
        return result

    def calc_size(self, value):
        return self._size_parser.calc_size(value) + sum(self._element_parser.calc_size(item) for item in value)

    def parse(self, buffer):
        size = self._size_parser.parse(buffer)
        idx = self._size_parser.calc_size(size)
        result = []
        for i in range(size):
            result.append(self._element_parser.parse(buffer[idx:]))
            idx += self._element_parser.calc_size(result[-1])
        return result
