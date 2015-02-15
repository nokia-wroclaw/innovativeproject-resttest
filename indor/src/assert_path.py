#-*- coding: utf-8 -*-
__author__ = 'Bartosz Zięba'

from command import Command
from command_factory import CommandFactory
from command_register import CommandRegister
from result import Error, Passed, Failed
from indor_exceptions import InvalidRelationalOperator, IndorSyntaxErrorWrongNumberOfArguments
import result
from relational_operators import compare_by_supposed_relational_operator


class AssertPath(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH"

    def __init__(self, result_collector):
        super(AssertPath, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise IndorSyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         'At least 2 arguments expected. ' + self.pretty_name +
                                                         ' is not valid command.', CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        url = path[0]
        next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
        path = path[2:]
        path.insert(0, url)
        next_step.parse(path)


class AssertPathExists(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH EXISTS"

    def __init__(self, result_collector):
        super(AssertPathExists, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 1:
            raise IndorSyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         'The path to check expected.')

        self.execute(path[0])

    def execute(self, url):
        doc = self.result_collector.get_response_ElementTree()
        if len(doc.findall(url)) > 0:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, "EXISTS", "NO EXISTS"))


class AssertPathContains(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH CONTAINS"

    def __init__(self, result_collector):
        super(AssertPathContains, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise IndorSyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(self.__class__.__name__))

        url = path[0]
        from command_factory import CommandFactory

        next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
        path = path[2:]
        path.insert(0, url)
        next_step.parse(path)


class AssertPathContainsAny(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH CONTAINS ANY"

    def __init__(self, result_collector):
        super(AssertPathContainsAny, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 2:
            raise IndorSyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        self.execute(path)

    def execute(self, path):
        doc = self.result_collector.get_response_ElementTree()
        for e in doc.findall(path[0]):
            if e.text is not None:
                if type(e.text) is 'unicode':
                    if path[1].decode('utf-8') in e.text.decode('utf-8'):
                        self.result_collector.add_result(Passed(self))
                        return
                else:
                    if path[1].decode('utf-8') in e.text:
                        self.result_collector.add_result(Passed(self))
                        return
        self.result_collector.add_result(Failed(self, "ASSERT PATH CONTAINS ANY", "NOP"))


class AssertPathContainsEach(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH CONTAINS EACH"

    def __init__(self, result_collector):
        super(AssertPathContainsEach, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise IndorSyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'At least 2 arguments expected')

        self.execute(path)

    def execute(self, path):
        doc = self.result_collector.get_response_ElementTree()
        for e in doc.findall(path[0]):
            if e.text is not None:
                if type(e.text) is 'unicode':
                    if path[1].decode('utf-8') in e.text.decode('utf-8'):
                        continue
                    else:
                        self.result_collector.add_result(Failed(self, "ASSERT PATH CONTAINS EACH", ""))
                        return
                else:
                    if path[1].decode('utf-8') in e.text:
                        continue
                    else:
                        self.result_collector.add_result(Failed(self, "ASSERT PATH CONTAINS EACH", ""))
                        return
            else:
                self.result_collector.add_result(Failed(self, "ASSERT PATH CONTAINS EACH", ""))
                return
        self.result_collector.add_result(Passed(self))


class AssertPathNodes(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH NODES"

    def __init__(self, result_collector):
        super(AssertPathNodes, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise IndorSyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        url = path[0]
        next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
        path = path[2:]
        path.insert(0, url)
        next_step.parse(path)


class AssertPathNodesCount(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH NODES COUNT"

    def __init__(self, result_collector):
        super(AssertPathNodesCount, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            raise IndorSyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'At least two arguments expected.')

        self.execute(path)

    def execute(self, path):
        try:
            relational_operator = path[1]
            expected = int(path[2])
            doc = self.result_collector.get_response_ElementTree()
            num = len(doc.findall(path[0]))
            if compare_by_supposed_relational_operator(num, relational_operator, expected):
                self.result_collector.add_result(Passed(self))
            else:
                self.result_collector.add_result(Failed(self, relational_operator + " " + path[2], num))

        except ValueError:
            self.result_collector.add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
        except InvalidRelationalOperator as e:
            self.result_collector.add_result(Error.from_exception(self, e))


class AssertPathFinal(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH FINAL"

    def __init__(self, result_collector):
        super(AssertPathFinal, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 1:
            raise IndorSyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'At least on argument expected.')

        self.execute(path)

    def execute(self, path):
        doc = self.result_collector.get_response_ElementTree()
        if len(doc.findall(path[0])) > 0 and len(doc.findall(path[0]+"/*")) == 0:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, "ASSERT PATH FINAL", "NOT FINAL"))