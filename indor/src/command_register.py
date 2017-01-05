from .indor_exceptions import ClassPropertyNotFound

from .command import Command
from .command_factory import CommandFactory


class CommandRegister(type(Command)):
    def __init__(cls, name, bases, dic):
        cls.property_name_for_printer = 'pretty_name'
        if cls.property_name_for_printer not in dic:
            raise ClassPropertyNotFound(name, cls.property_name_for_printer)
        super(CommandRegister, cls).__init__(name, bases, dic)
        CommandFactory().add_class(name, cls)
