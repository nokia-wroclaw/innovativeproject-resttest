__author__ = 'Bartosz Zięba'

from .command import Command
from .command_factory import CommandFactory
from .command_register import CommandRegister
from .indor_exceptions import SyntaxErrorWrongNumberOfArguments


class Set(Command, metaclass=CommandRegister):
    pretty_name = "SET"

    def __init__(self, result_collector):
        super(Set, self).__init__(result_collector)

    def parse(self, path):
        if len(path) <= 1:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                         self.__class__.__name__))
        else:
            next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
            next_step.parse(path[1:])


class SetParser(Command, metaclass=CommandRegister):
    pretty_name = "SET PARSER"

    def __init__(self, result_collector):
        super(SetParser, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 1:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                         self.__class__.__name__))
        else:
            self.result_collector.set_parser(path[0])