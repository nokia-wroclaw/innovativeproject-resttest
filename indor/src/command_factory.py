from singleton import Singleton


class CommandFactory:
    __metaclass__ = Singleton

    def __init__(self):
        self.dict = {}

    def add_class(self, class_name, class_type):
        self.dict[class_name] = class_type

    def get_class(self, prefix, suffix, result_collector):
        new_class_name = prefix + suffix.title()
        return self.dict[new_class_name](result_collector)