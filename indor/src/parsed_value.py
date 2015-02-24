# coding=utf-8
__author__ = 'Sławomir Domagała'


class ParsedValue:
    def __init__(self, parsing_object, value, description):
        self.parsing_object = parsing_object
        self.value = value
        self.description = description
