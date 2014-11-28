from command import Command
from assert_ import Assert
from connect import Connect

ASSERT_NAME = 'ASSERT'
SCENARIO_NAME = 'SCENARIO'

# Base class for all tests
class Test(Command):
    def parse(self, path):
        argument = path[0]

        if argument == ASSERT_NAME:
            next_step = Assert()
            next_step.parse(path[1:])
        elif argument in ['GET', 'POST', 'PUT', 'DELETE']:
            next_step = Connect()
            next_step.parse(path[0:])

        return False