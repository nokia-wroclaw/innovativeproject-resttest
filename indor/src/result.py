class Result:
    def __init__(self, class_instance):
        self.class_name = class_instance.__class__.__name__


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