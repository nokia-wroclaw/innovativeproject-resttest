# coding=utf-8
from asserts import *
from assert_path import *


class Assert(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT"

    def __init__(self, result_collector):
        super(Assert, self).__init__(result_collector)

    def parse(self, path):
        for i in range(0, len(path)):
            path[i] = self.result_collector.use_variables(path[i])

        if len(path) == 0:
            self.result_collector.add_result(Error(self, "Za mało argumentów"))
            return

        CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector).parse(path[1:])
