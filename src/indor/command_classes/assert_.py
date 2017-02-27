import importlib

from .command_response import *
from ..indor_exceptions import SyntaxErrorWrongNumberOfArguments
from ..parsing_exception import ParsingException
from ..result import Passed, Failed
from ..tools import transform_nested_array, get_parent_module_name

importlib.import_module(".command_request", package=get_parent_module_name(__name__))
importlib.import_module(".commands", package=get_parent_module_name(__name__))


class Assert(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT"

    def __init__(self, result_collector):
        super(Assert, self).__init__(result_collector)

    def parse(self, path):
        path = transform_nested_array(path, self.result_collector.use_variables)

        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                    hints=CommandFactory().get_class_children(
                                                        self.__class__.__name__))
        command = CommandFactory().get_class("Command", path[0], self.result_collector)
        try:
            computed, parsed = command.parse(path[1:])
            if computed == parsed.value:
                self.result_collector.add_result(Passed(parsed.parsing_object, parsed.description))
            else:
                self.result_collector.add_result(Failed(parsed.parsing_object, parsed.description, computed))
        except ParsingException as e:
            self.result_collector.add_result(Error(e.parsing_object, e.message))
