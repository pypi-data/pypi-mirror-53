from generic_struct.parsers import Parser, validated_parser


@validated_parser
class DelimitedListParser(Parser):
    """
    a parser for a list of objects with a delimiter value at the end
    """
    _TYPES = list,

    def __init__(self, element_parser, delimiter, delimiter_parser):
        """
        :param element_parser: a parser for the elements in the list
        :type element_parser: C{Parser}
        :param delimiter: an object that marks the end of the list
        :type delimiter: C{object}
        :param delimiter_parser: a parser fot the delimiter
        :type delimiter_parser: C{Parser}
        """
        self._element_parser = element_parser
        self._delimiter = delimiter
        self._delimiter_parser = delimiter_parser

    def generate_buffer(self, value):
        result = b''
        for element in value:
            result += self._element_parser.generate_buffer(element)
        result += self._delimiter_parser.generate_buffer(self._delimiter)
        return result

    def calc_size(self, value):
        return sum(self._element_parser.calc_size(element) for element in value) + \
               self._delimiter_parser.calc_size(self._delimiter)

    def parse(self, buffer):
        result = []
        idx = 0
        while buffer[idx:].index(self._delimiter_parser.generate_buffer(self._delimiter)) > 0:
            result.append(self._element_parser.parse(buffer[idx:]))
            idx += self._element_parser.calc_size(result[-1])
        return result



