#-*- coding: utf-8 -*-
__author__ = 'Bartosz Zięba'

from command import Command
from command_factory import CommandFactory
from command_register import CommandRegister
from result import Error, Passed, Failed
from indor_exceptions import InvalidRelationalOperator
import result
from relational_operators import compare_by_relational_operator
from relational_operators import extract_relational_operator


class AssertPath(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH"

    def __init__(self, result_collector):
        super(AssertPath, self).__init__(result_collector)

    def parse(self, path):
        try:
            # TODO: Bartosz Zięba - brak konsekwencji - raz wszystko w try, raz tylko 2 linijki
            if len(path) < 2:
                self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            else:
                url = path[0]
                next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
                path = path[2:]
                path.insert(0, url)
                next_step.parse(path)
        except Exception as e:
            self.result_collector.add_result(Error(self, e.message))


class AssertPathExists(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH EXISTS"

    def __init__(self, result_collector):
        super(AssertPathExists, self).__init__(result_collector)

    def parse(self, path):
        try:
            if len(path) != 1:
                self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            else:
                self.execute(path[0])
        except Exception as e:
            self.result_collector.add_result(Error(self, e.message))

    def execute(self, url):
        doc = self.result_collector.get_response_ET()
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
        try:
            # TODO: Bartosz Zięba - brak konsekwencji - raz wszystko w try, raz tylko 2 linijki
            if len(path) < 2:
                self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            else:
                url = path[0]
                from command_factory import CommandFactory

                next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
                path = path[2:]
                path.insert(0, url)
                next_step.parse(path)
        except Exception as e:
            self.result_collector.add_result(Error(self, e.message))


class AssertPathContainsAny(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH CONTAINS ANY"

    def __init__(self, result_collector):
        super(AssertPathContainsAny, self).__init__(result_collector)

    def parse(self, path):
        try:
            if len(path) != 2:
                self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            else:
                self.execute(path)
        except Exception as e:
            self.result_collector.add_result(Error(self, e.message))

    def execute(self, path):
        doc = self.result_collector.get_response_ET()
        for e in doc.findall(path[0]):
            # TODO - Bartosz Zięba - PEP-8, magiczne zmienne, duplikacja kodu
            if e.text != None:
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
        try:
            if len(path) != 2:
                self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            else:
                self.execute(path)
        except Exception as e:
            self.result_collector.add_result(Error(self, e.message))

    def execute(self, path):
        doc = self.result_collector.get_response_ET()
        for e in doc.findall(path[0]):
            # TODO: PEP-8 Bartosz Zięba - wszędzie zamienić na e.text is not None (nie porównuje się z None)
            # TODO: Bartosz Zięba - Magiczne stringi 'utf-8', 'unicode'
            # TODO: Bartosz Zięba - Nie da się tego uwspólnić (duplikacja kodu w tym wielkim if-elsie)
            if e.text != None:
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
        # TODO: Bartosz Zięba - Brak konsekwencji - raz wszystko w try, raz tylko 2 linijki w try
        # TODO: Bartosz Zięba - Łapanie Exception jest chyba bardzo ogólne
        try:
            if len(path) < 2:
                self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            else:
                url = path[0]
                next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
                path = path[2:]
                path.insert(0, url)
                next_step.parse(path)
        except Exception as e:
            self.result_collector.add_result(Error(self, e.message))


class AssertPathNodesCount(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH NODES COUNT"

    def __init__(self, result_collector):
        super(AssertPathNodesCount, self).__init__(result_collector)

    def parse(self, path):
        try:
            if len(path) < 2:
                self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            else:
                self.execute(path)
        except Exception as e:
            self.result_collector.add_result(Error(self, e.message))

    def execute(self, path):
        try:
            relational_operator = extract_relational_operator(path[1])
            expected = int(path[2])
        except ValueError:
            self.result_collector.add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
            return
        except InvalidRelationalOperator as e:
            self.result_collector.add_result(Error(self, e.message))
            return
        doc = self.result_collector.get_response_ET()
        num = len(doc.findall(path[0]))
        if compare_by_relational_operator(num, relational_operator, expected):
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, relational_operator + " " + path[2], num))


class AssertPathFinal(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH FINAL"

    def __init__(self, result_collector):
        super(AssertPathFinal, self).__init__(result_collector)

    def parse(self, path):
        try:
            # TODO: Bartosz Zięba - Wprowadzenie użytkownika w błąd
            # len(path) != 1 nie oznacza, że ERROR_NOT_ENOUGH_ARGUMENTS
            if len(path) != 1:
                self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            else:
                self.execute(path)
        except Exception as e:
            self.result_collector.add_result(Error(self, e.message))

    def execute(self, path):
        # TODO: Bartosz Zięba - Dlaczego funkcja jest nazwana get_response_ET? Co to jest ET?
        doc = self.result_collector.get_response_ET()
        if len(doc.findall(path[0])) > 0 and len(doc.findall(path[0]+"/*")) == 0:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, "ASSERT PATH FINAL", "NOT FINAL"))