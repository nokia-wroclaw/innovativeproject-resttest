# coding=utf-8
from asserts import *


class Assert(Command):
    def parse(self, path):
        if len(path) == 0:
            ResultCollector().add_result(Error(self, "Za mało argumentów"))
            return

        CommandFactory().get_class(self.__class__.__name__, path[0]).parse(path[1:])
