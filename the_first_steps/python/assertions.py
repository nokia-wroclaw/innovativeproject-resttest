import re
from abc import ABCMeta, abstractmethod
import requests

__author__ = 'Damian Mirecki'

class AbstractAction():
    __metaclass__ = ABCMeta

    request = None
    result = None

    @abstractmethod
    def check(self): pass

    def printBool(self, bool):
        print bool


class AssertResponseIsJson(AbstractAction):
    def check(self):
        self.printBool(bool(re.search('.*json.*', AbstractAction.request.headers['content-type'])))


class AssertSuccess(AbstractAction):
    def check(self):
        self.printBool(AbstractAction.request.status_code == requests.codes.ok)


class AssertContainsKey(AbstractAction):
    def __init__(self, name):
        self.name = name

    def check(self):
        self.printBool(self.name in AbstractAction.result)


class AssertContainsValueWithType(AbstractAction):
    def __init__(self, name, type):
        self.type = type
        self.name = name

    def check(self):
        if self.type == "array":
            self.printBool(isinstance(AbstractAction.result[self.name], list))