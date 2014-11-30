# coding=utf-8
from asserts import *


class Assert(Command):
    __metaclass__ = CommandRegister

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, "Za mało argumentów"))
            return

        CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector).parse(path[1:])
