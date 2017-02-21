from ..command_classes.handle import Handle
from ..command_classes.assign import Assign
from ..command import Command
from ..command_classes.assert_ import Assert
from ..command_classes.connect import Connect
from ..indor_exceptions import SyntaxErrorClassNotExists, SyntaxErrorWrongNumberOfArguments
from ..result import Error
from .scenario import Scenario
from ..select_parser import Set

ASSERT_NAME = 'ASSERT'
SCENARIO_NAME = 'SCENARIO'
ASSIGN_NAME = 'ASSIGN'
REPEATED_SCENARIO_NAME = 'REPEATED_SCENARIO'
SET_NAME = 'SET'
HANDLE_NAME = 'HANDLE'

http_request_types = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']


class Test(Command):

    pretty_name = ""

    def __init__(self, result_collector):
        super(Test, self).__init__(result_collector)

    def parse(self, path):
        argument = path[0]

        try:
            if argument == SCENARIO_NAME:
                next_step = Scenario(self.result_collector)
                next_step.parse(path[1:])
            elif argument == REPEATED_SCENARIO_NAME:
                next_step = Scenario(self.result_collector)
                next_step.parse(path[2:], path[1])
            elif argument == ASSIGN_NAME:
                next_step = Assign(self.result_collector)
                next_step.parse(path[1:])
            else:
                if self.result_collector.execute_current_scenario:
                    if argument == ASSERT_NAME:
                        next_step = Assert(self.result_collector)
                        next_step.parse(path[1:])
                    elif argument in http_request_types or argument[0] in http_request_types:
                        next_step = Connect(self.result_collector)
                        next_step.parse(path[0:])
                    elif argument == SET_NAME:
                        next_step = Set(self.result_collector)
                        next_step.parse(path[1:])
                    elif argument == HANDLE_NAME or argument[0] == HANDLE_NAME:
                        next_step = Handle(self.result_collector)
                        next_step.parse(path[0:])
        except (SyntaxErrorClassNotExists, SyntaxErrorWrongNumberOfArguments) as e:
            self.result_collector.add_result(Error.syntax_error(self, path, str(e)))
