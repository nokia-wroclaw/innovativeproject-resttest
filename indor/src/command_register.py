__author__ = 'slawomir'
from command import Command
from command_factory import CommandFactory


class CommandRegister(Command.__metaclass__):
    def __init__(cls, name, bases, dic):
        super(CommandRegister, cls).__init__(name, bases, dic)
        CommandFactory().add_class(name, cls)
