__author__ = 'Bartek'

from singleton import Singleton

class XmlTreeFactory:
    __metaclass__ = Singleton

    def __init__(self):
        self.dict = {}

    def add_class(self, class_name, class_type):
        self.dict[class_name] = class_type
        print class_name

    def get_class(self, contentType):
        # TODO Bartek: troszke malo faktorkowo ale poprawie
        if "xml" in contentType:
            class_name = "TextXml"
        elif "json" in contentType:
            class_name = "TextJson"
        else:
            class_name = "None"
        if class_name not in self.dict:
            return None
        return self.dict[class_name]()