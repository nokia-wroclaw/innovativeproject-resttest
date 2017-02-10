from command import Command
from command_register import CommandRegister


class Handle(Command, metaclass=CommandRegister):
    pretty_name = "HANDLING REQUEST"

    def __init__(self, result_collector):
        super(Handle, self).__init__(result_collector)

    def parse(self, path):
        pass