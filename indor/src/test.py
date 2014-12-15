from command import Command
from assert_ import Assert
from connect import Connect
from scenario import Scenario

ASSERT_NAME = 'ASSERT'
SCENARIO_NAME = 'SCENARIO'

http_request_types = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']

class Test(Command):
    def __init__(self, result_collector):
        super(Test, self).__init__(result_collector)

    def parse(self, path):
        argument = path[0]

        if argument == ASSERT_NAME:
            next_step = Assert(self.result_collector)
            next_step.parse(path[1:])
        elif argument in http_request_types or argument[0] in http_request_types:
            next_step = Connect(self.result_collector)
            next_step.parse(path[0:])
        elif argument == SCENARIO_NAME:
            next_step = Scenario(self.result_collector)
            next_step.parse(path[1:])

        return False