# coding=utf-8
__author__ = 'Sławomir Domagała'


class TestResults:
    def __init__(self, name):
        self.name = name
        self.results = []

    def add_result(self, result):
        self.results.append(result)