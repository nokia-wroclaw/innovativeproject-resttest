__author__ = 'slawomir'
from command_factory import CommandFactory
from abc import ABCMeta


class CommandRegister(ABCMeta):
    def __init__(cls, name, bases, dic):
        super(CommandRegister, cls).__init__(name, bases, dic)
        CommandFactory().add_class(name, cls)
