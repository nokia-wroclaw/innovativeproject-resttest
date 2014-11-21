__author__ = 'slawomir'

from abc import ABCMeta, abstractmethod


class Command(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, path):
        pass