from abc import ABCMeta, abstractmethod


class Command(object, metaclass=ABCMeta):
    def __init__(self, result_collector):
        self.result_collector = result_collector

    @abstractmethod
    def parse(self, path):
        pass