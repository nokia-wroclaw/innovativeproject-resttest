import re
from .indor_exceptions import SyntaxErrorClassNotExists
from .singleton import Singleton


class CommandFactory(object, metaclass=Singleton):
    def __init__(self):
        self.dict = {}

    def add_class(self, class_name, class_type):
        self.dict[class_name] = class_type

    def get_class(self, prefix, suffix, result_collector):
        new_class_name = prefix + suffix.title()

        if new_class_name not in self.dict:
            raise SyntaxErrorClassNotExists(prefix, suffix, new_class_name)

        return self.dict[new_class_name](result_collector)

    def get_class_children(self, class_name):
        prog = re.compile(class_name + "[A-Za-z]+")
        return [child_type.pretty_name for child_name, child_type in self.dict.iteritems() if prog.match(child_name)]