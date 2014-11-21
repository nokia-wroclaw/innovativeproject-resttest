__author__ = 'slawomir'

from abc import ABCMeta, abstractmethod
from result import Result


class Command(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.result = Result()

    @abstractmethod
    def parse(self, path):
        pass