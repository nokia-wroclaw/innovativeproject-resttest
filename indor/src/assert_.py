from command import Command
from asserts import *

# This class inherits from the class Test
# Base class for Assertions

class Assert(Command):
    def parse(self, path):
        # Convert all arguments to CamelCase
        arguments = map(lambda x: x.title(), path)

        new_class_name = self.__class__.__name__ + arguments[0]

        next_step = eval(new_class_name + "()")
        next_step.parse(arguments[1:])
