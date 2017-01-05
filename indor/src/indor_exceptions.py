class KeywordNotFound(Exception):
    def __init__(self, keyword):
        super(KeywordNotFound, self).__init__("Incorrect keyword: " + keyword)


class SyntaxErrorClassNotExists(Exception):
    def __init__(self, prefix, suffix, new_class_name):
        super(SyntaxErrorClassNotExists, self).__init__(
            "Class " + prefix + " got " + suffix + " and tried to instance class " + new_class_name + "." +
            " This class not existed. There might by a typo or you have to implement it.")


class SyntaxErrorWrongNumberOfArguments(Exception):
    def __init__(self, class_name, condition_description="", hints=None):
        message = "Error detected at " + class_name + ". Wrong number of arguments. " + condition_description

        if hints is not None:
            message += " Did you mean " + ", ".join(hints) + '?'

        super(SyntaxErrorWrongNumberOfArguments, self).__init__(message)


class TypeRequestNotFound(Exception):
    pass


class URLNotFound(Exception):
    def __init__(self, url):
        super(URLNotFound, self).__init__("Incorrect URL Address: " + url)


class InvalidRelationalOperator(Exception):
    def __init__(self, keyword):
        super(InvalidRelationalOperator, self).__init__("Invalid relational operator: " + keyword)


# Internal exceptions, not for an user, but for a developer
class ClassPropertyNotFound(Exception):
    def __init__(self, class_name, property_name):
        super(ClassPropertyNotFound, self).__init__("Property {} not found in {}".format(property_name, class_name))


class InvalidRepeatParameters(Exception):
    def __init__(self, params):
        super(InvalidRepeatParameters, self).__init__("Invalid parameters for REPEAT statement: " + params)