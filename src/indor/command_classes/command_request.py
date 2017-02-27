from .. import result
from ..command import Command
from ..command_factory import CommandFactory
from ..command_register import CommandRegister
from ..indor_exceptions import SyntaxErrorWrongNumberOfArguments
from ..parsed_value import ParsedValue
from ..parsing_exception import ParsingException


class CommandRequest(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT REQUEST"

    def __init__(self, result_collector):
        super(CommandRequest, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
        return next_step.parse(path[0:1]+path[2:])


class CommandRequestHandled(Command, metaclass=CommandRegister):
    pretty_name = "REQUEST HANDLED"

    def __init__(self, result_collector):
        super(CommandRequestHandled, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))
        if path[0] not in self.result_collector.requests:
            raise ParsingException(self, result.ERROR_REQUEST_NOT_FOUND)

        computed = self.result_collector.requests[path[0]].handled
        parsed = ParsedValue(self, True, path[0] + " to be HANDLED")
        return computed, parsed


class CommandRequestMethod(Command, metaclass=CommandRegister):
    pretty_name = "REQUEST METHOD"

    def __init__(self, result_collector):
        super(CommandRequestMethod, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))
        if path[0] not in self.result_collector.requests:
            raise ParsingException(self, result.ERROR_REQUEST_NOT_FOUND)

        computed = self.result_collector.requests[path[0]].request_method
        parsed = ParsedValue(self, path[1], "Request " + path[0] + " method is " + path[1])
        return computed, parsed
