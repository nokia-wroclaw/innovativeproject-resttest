# coding=utf-8
import re
from command import Command
from command_factory import CommandFactory
from command_register import CommandRegister
from indor_exceptions import SyntaxErrorWrongNumberOfArguments
from parsing_exception import ParsingException
from result import Error
import result


class Assign(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSIGN"

    def __init__(self, result_collector):
        super(Assign, self).__init__(result_collector)

    def parse(self, path):
        for i in range(1, len(path)-1):
            path[i] = self.result_collector.use_variables(path[i])

        if len(path) <= 1:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                          self.__class__.__name__))

        try:
            if path[1].lower() == "text" or path[1].lower() == "cookie":
                command = CommandFactory().get_class("Command", path[1], self.result_collector)
                computed, parsed = command.parse(path[2:])
                self.result_collector.add_variable(path[0], computed)
            else:
                command = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
                command.parse(path[2:])
                self.result_collector.add_variable(path[0], command.execute())
        except ParsingException as e:
            self.result_collector.add_result(Error(e.parsing_object, e.message))


class AssignResponse(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSIGN RESPONSE"

    def __init__(self, result_collector):
        super(AssignResponse, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        self.command = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        self.command.parse(path[1:])

    def execute(self):
        return self.command.execute()


class AssignResponseStatus(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSIGN RESPONSE STATUS"

    def __init__(self, result_collector):
        super(AssignResponseStatus, self).__init__(result_collector)

    def parse(self, path):
        pass

    def execute(self):
        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        return str(response.status_code)