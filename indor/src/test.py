from command import Command
from assert_ import Assert
from connect import Connect
from scenario import Scenario

ASSERT_NAME = 'ASSERT'
SCENARIO_NAME = 'SCENARIO'

# Base class for all tests
class Test(Command):


    def __init__(self, test_runner):
        self.test_runner = test_runner


    def parse(self, path):
        argument = path[0]

        if argument == ASSERT_NAME:
            next_step = Assert()
            next_step.parse(path[1:])
        elif argument in ['GET', 'POST', 'PUT', 'DELETE']:
            next_step = Connect()
            next_step.parse(path[0:])
        elif argument == SCENARIO_NAME:
            next_step = Scenario(self.test_runner, path[1:])

        return False