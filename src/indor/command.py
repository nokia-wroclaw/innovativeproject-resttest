from abc import ABCMeta, abstractmethod


class Command(object, metaclass=ABCMeta):
    def __init__(self, result_collector):
        self.result_collector = result_collector

    @abstractmethod
    def parse(self, path):
        """

        :param path: list of args to execute one statement
        :type path: list
        :return:
        """
        pass
