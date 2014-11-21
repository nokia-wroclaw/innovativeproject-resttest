from singleton import Singleton


class ResultCollector(object):
    __metaclass__ = Singleton

    def __init__(self, test_runner=None):
        if test_runner is None:
            raise Exception("test_result can't be none")
        self.test_runner = test_runner

    def set_response(self, response):
        self.test_runner.response = response

    def get_response(self):
        return self.test_runner.response

    def add_result(self, result):
        self.test_runner.tested_classes.append(result)