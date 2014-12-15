__author__ = 'Bartek'
from abc import ABCMeta, abstractmethod


class XmlTree(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, xml):
        pass