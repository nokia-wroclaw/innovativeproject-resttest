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
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


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
        parsed = ParsedValue(self, True, "HANDLED")
        return computed, parsed
