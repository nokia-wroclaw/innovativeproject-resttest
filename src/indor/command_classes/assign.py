from ..command import Command
from ..command_factory import CommandFactory
from ..command_register import CommandRegister
from ..indor_exceptions import SyntaxErrorWrongNumberOfArguments
from ..parsing_exception import ParsingException
from ..result import Error


class Assign(Command, metaclass=CommandRegister):
    pretty_name = "ASSIGN"

    def __init__(self, result_collector):
        super(Assign, self).__init__(result_collector)

    def parse(self, path):
        for i in range(1, len(path) - 1):
            path[i] = self.result_collector.use_variables(path[i])

        if len(path) <= 1:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))

        try:
            command = CommandFactory().get_class("Command", path[1], self.result_collector)
            computed, parsed = command.parse(path[2:])
            self.result_collector.add_variable(path[0], computed)
        except ParsingException as e:
            self.result_collector.add_result(Error(e.parsing_object, e.message))
