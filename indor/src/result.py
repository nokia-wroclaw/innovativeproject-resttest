# coding=utf-8

ERROR_NUMBER_EXPECTED = "Oczekiwano liczby"
ERROR_NOT_ENOUGH_ARGUMENTS = "Za mało argumentów"
ERROR_WRONG_CONTENT_TYPE = "Zły typ contentu"


class Result:
    def __init__(self, class_instance):
        self.pretty_name = class_instance.__class__.pretty_name


class Passed(Result):
    def __init__(self, class_instance):
        Result.__init__(self, class_instance)


class Failed(Result):
    def __init__(self, class_instance, expected, actual):
        Result.__init__(self, class_instance)
        self.expected = expected
        self.actual = actual


class Error(Result):
    def __init__(self, class_instance, error):
        Result.__init__(self, class_instance)
        self.error = error