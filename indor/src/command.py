__author__ = 'slawomir'
from abc import ABCMeta, abstractmethod


class Command(object):
    __metaclass__ = ABCMeta

    def __init__(self, result_collector):
        self.result_collector = result_collector

    @abstractmethod
    def parse(self, path):
        pass