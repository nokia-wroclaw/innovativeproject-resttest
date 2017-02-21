from .. import result
from ..command import Command
from ..command_factory import CommandFactory
from ..command_register import CommandRegister
from ..indor_exceptions import InvalidRelationalOperator, SyntaxErrorWrongNumberOfArguments
from ..parsed_value import ParsedValue
from ..parsing_exception import ParsingException
from ..relational_operators import compare_by_supposed_relational_operator
from .. import select_parser # important import


class CommandPath(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT PATH"

    def __init__(self, result_collector):
        super(CommandPath, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    'At least 2 arguments expected. ' + self.pretty_name +
                                                    ' is not valid command.',
                                                    CommandFactory().get_class_children(self.__class__.__name__))

        url = path[0]
        next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
        path = path[2:]
        path.insert(0, url)
        return next_step.parse(path)


class CommandPathExists(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT PATH EXISTS"

    def __init__(self, result_collector):
        super(CommandPathExists, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 1:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    'The path to check expected.')

        url = path[0]
        doc = self.result_collector.get_response_ElementTree()

        computed = len(doc.findall(url)) > 0
        parsed = ParsedValue(self, True, "NO EXISTS")
        return computed, parsed


class CommandPathContains(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT PATH CONTAINS"

    def __init__(self, result_collector):
        super(CommandPathContains, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(self.__class__.__name__))

        url = path[0]

        next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
        path = path[2:]
        path.insert(0, url)
        return next_step.parse(path)


class CommandPathContainsAny(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT PATH CONTAINS ANY"

    def __init__(self, result_collector):
        super(CommandPathContainsAny, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))
        parsed = ParsedValue(self, True, "PATH CONTAINS ANY")
        computed = False

        doc = self.result_collector.get_response_ElementTree()
        for e in doc.findall(path[0]):
            if e.text is not None:
                if type(e.text) is 'unicode':
                    if path[1].decode('utf-8') in e.text.decode('utf-8'):
                        computed = True
                        break
                else:
                    if path[1].decode('utf-8') in e.text:
                        computed = True
                        break
        return computed, parsed


class CommandPathContainsEach(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT PATH CONTAINS EACH"

    def __init__(self, result_collector):
        super(CommandPathContainsEach, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'At least 2 arguments expected')

        parsed = ParsedValue(self, True, "PATH CONTAINS EACH")
        computed = True

        doc = self.result_collector.get_response_ElementTree()
        for e in doc.findall(path[0]):
            if e.text is not None:
                if type(e.text) is 'unicode':
                    text = e.text.decode('utf-8')
                else:
                    text = e.text

                if path[1].decode('utf-8') not in text:
                    computed = False
                    break
            else:
                computed = False
                break
        return computed, parsed


class CommandPathNodes(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT PATH NODES"

    def __init__(self, result_collector):
        super(CommandPathNodes, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))

        url = path[0]
        next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
        path = path[2:]
        path.insert(0, url)
        return next_step.parse(path)


class CommandPathNodesCount(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT PATH NODES COUNT"

    def __init__(self, result_collector):
        super(CommandPathNodesCount, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 1 and len(path) != 3:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'Two or three arguments expected.')

        try:
            doc = self.result_collector.get_response_ElementTree()
            actual = len(doc.findall(path[0]))

            if len(path) == 1:
                actual, ParsedValue(self, None, "")

            relational_operator = path[1]
            expected = int(path[2])

            parsed = ParsedValue(self, True, relational_operator + " " + path[2])
            computed = compare_by_supposed_relational_operator(actual, relational_operator, expected)
            return computed, parsed
        except ValueError:
            raise ParsingException(self, result.ERROR_NUMBER_EXPECTED)
        except InvalidRelationalOperator as e:
            raise ParsingException(self, e)


class CommandPathFinal(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT PATH FINAL"

    def __init__(self, result_collector):
        super(CommandPathFinal, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 1:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'At least on argument expected.')

        doc = self.result_collector.get_response_ElementTree()
        computed = len(doc.findall(path[0])) > 0 and len(doc.findall(path[0] + "/*")) == 0
        parsed = ParsedValue(self, True, "PATH FINAL")
        return computed, parsed
