from abc import ABCMeta, abstractmethod


class XmlTree(object, metaclass=ABCMeta):
    @abstractmethod
    def parse(self, xml):
        pass