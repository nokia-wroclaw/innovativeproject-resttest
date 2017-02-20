import importlib

from ..command import Command
from ..command_factory import CommandFactory
from ..command_register import CommandRegister
from ..indor_exceptions import SyntaxErrorWrongNumberOfArguments
from ..tools import transform_nested_array, get_parent_module_name

importlib.import_module(".handle_request", package=get_parent_module_name(__name__))


class Handle(Command, metaclass=CommandRegister):
    pretty_name = "HANDLING"

    def __init__(self, result_collector):
        super(Handle, self).__init__(result_collector)

    def parse(self, path):
        path = transform_nested_array(path, self.result_collector.use_variables)

        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))

        if not isinstance(path[0], str):
            command = CommandFactory().get_class("Handle", path[0][1], self.result_collector)
        else:
            command = CommandFactory().get_class("Handle", path[1], self.result_collector)

        command.parse(path[0:])
