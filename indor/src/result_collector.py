class Singleton(type):
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


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