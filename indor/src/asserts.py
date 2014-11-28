# coding=utf-8
from command import Command
from command_factory import CommandFactory
from result import Error, Passed, Failed
from indor_exceptions import InvalidRelationalOperator
import result
from result_collector import ResultCollector
from requests.structures import CaseInsensitiveDict


def compare_by_relational_operator(actual, relational_operator, expected):
    return eval(str(actual) + " " + relational_operator + " " + str(expected))


def extract_relational_operator(supposed_operator):
    """
    Function removes extra spaces, check if given operator is valid
    and replace ambiguous operator, e.g. replace "=" with "=="

    :param supposed_operator:
    :type supposed_operator: str
    :return: :rtype: str :raise InvalidRelationalOperator:
    """
    equality_operators = ["=", "=="]
    inequality_operators = ["!=", "<>"]
    valid_operators = ["<", ">", "<=", ">="]

    supposed_operator = supposed_operator.strip()

    if supposed_operator in equality_operators:
        return "=="

    if supposed_operator in inequality_operators:
        return "!="

    if not supposed_operator in valid_operators:
        raise InvalidRelationalOperator("got '" + supposed_operator + "' but only " + (
            valid_operators + equality_operators + inequality_operators).__str__() + " is accepted")

    return supposed_operator


class AssertResponseRedirects(Command):
    def parse(self, path):
        next_step = CommandFactory().get_class(self.__class__.__name__, path[0])
        next_step.parse(path[1:])
CommandFactory().add_class(AssertResponseRedirects.__name__, AssertResponseRedirects)


class AssertResponseRedirectsCount(Command):
    def parse(self, path):
        self.execute(path)

    def execute(self, args):
        if len(args) < 2:
            ResultCollector().add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        try:
            relational_operator = extract_relational_operator(args[0])
            expected = int(args[1])
        except ValueError:
            ResultCollector().add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
            return
        except InvalidRelationalOperator as e:
            ResultCollector().add_result(Error(self, e.message))
            return

        actual = len(ResultCollector().get_response().history)

        if compare_by_relational_operator(actual, relational_operator, expected):
            ResultCollector().add_result(Passed(self))
        else:
            ResultCollector().add_result(Failed(self, relational_operator + " " + args[1], str(actual)))
CommandFactory().add_class(AssertResponseRedirectsCount.__name__, AssertResponseRedirectsCount)


class AssertResponse(Command):
    def parse(self, path):
        if len(path) == 0:
            ResultCollector().add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0])
        next_step.parse(path[1:])
CommandFactory().add_class(AssertResponse.__name__, AssertResponse)


class AssertResponseNot(Command):
    def parse(self, path):
        if len(path) == 0:
            ResultCollector().add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0])
        next_step.parse(path[1:])
CommandFactory().add_class(AssertResponseNot.__name__, AssertResponseNot)


class AssertResponseStatus(Command):
    def __init__(self):
        super(AssertResponseStatus, self).__init__()
        self.mapping = CaseInsensitiveDict()
        self.mapping["Ok"] = 200
        self.mapping["Not found"] = 404


    def map_status_code(self, status):
        """

        author Damian Mirecki

        :param status
        :return:
        :rtype: int
        :raise LookupError: When status is not implemented yet.
        """

        # TODO: Catching any exceptions and errors.
        if not status in self.mapping:
            raise LookupError("Status " + status + " not found in " + self.mapping.__str__())

        return self.mapping[status]

    def parse(self, path):
        self.execute(path)

    def execute(self, args):
        status = args[0]

        if not status.isdigit():
            try:
                status = self.map_status_code(status)
            except LookupError as e:
                ResultCollector().add_result(Error(self, e))
                return

        actual = ResultCollector().get_response().status_code
        expected = int(status)
        if actual == expected:
            ResultCollector().add_result(Passed(self))
        else:
            ResultCollector().add_result(Failed(self, expected, actual))
CommandFactory().add_class(AssertResponseStatus.__name__, AssertResponseStatus)


class AssertResponseType(Command):
    def parse(self, path):
        if len(path) == 0:
            ResultCollector().add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0])
        next_step.parse(path[1:])
CommandFactory().add_class(AssertResponseType.__name__, AssertResponseType)


class AssertResponseTypeJson(Command):
    def parse(self, path):
        self.execute()

    def execute(self):
        try:
            ResultCollector().get_response().json()
        except ValueError:
            ResultCollector().add_result(Failed(self, "json", "not json"))
        else:
            ResultCollector().add_result(Passed(self))
CommandFactory().add_class(AssertResponseTypeJson.__name__, AssertResponseTypeJson)


class AssertResponseLength(Command):
    def parse(self, path):
        if path[0] == ">":
            next_step = AssertResponseLengthGreater()
            next_step.parse(path[1:])
        else:
            ResultCollector().add_result(Error(self, "Bad param or not implemented yet"))
CommandFactory().add_class(AssertResponseLength.__name__, AssertResponseLength)


class AssertResponseLengthGreater(Command):
    def parse(self, path):
        self.execute(path)

    def execute(self, args):
        if len(args) == 0:
            ResultCollector().add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        try:
            expected_content_length = int(args[0])
        except ValueError as e:
            ResultCollector().add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
            return

        if 'content-length' in ResultCollector().get_response().headers:
            content_length = int(ResultCollector().get_response().headers['content-length'])
        else:
            content_length = len(ResultCollector().get_response().content)
        if content_length > expected_content_length:
            ResultCollector().add_result(Passed(self))
        else:
            ResultCollector().add_result(Failed(self, "> " + args[0], content_length))
CommandFactory().add_class(AssertResponseLengthGreater.__name__, AssertResponseLengthGreater)


# Is response empty?
class AssertResponseEmpty(Command):
    def parse(self, path):
        self.execute()

    def execute(self):
        if len(ResultCollector().get_response().content) != 0:
            ResultCollector().add_result(Failed(self, "`EMPTY`", "`NOT EMPTY`"))
        else:
            ResultCollector().add_result(Passed(self))
CommandFactory().add_class(AssertResponseEmpty.__name__, AssertResponseEmpty)


class AssertResponseNotEmpty(Command):
    def parse(self, path):
        self.execute()

    def execute(self):
        if len(ResultCollector().get_response().content) == 0:
            ResultCollector().add_result(Failed(self, "`NOT EMPTY`", "`EMPTY`"))
        else:
            ResultCollector().add_result(Passed(self))
CommandFactory().add_class(AssertResponseNotEmpty.__name__, AssertResponseNotEmpty)


# Check Time of Response
class AssertResponseTime(Command):
    def __init__(self):
        super(AssertResponseTime, self).__init__()

    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        raise Exception("Not implemented yet")
CommandFactory().add_class(AssertResponseTime.__name__, AssertResponseTime)


# ??
class AssertPath(Command):
    def __init__(self):
        super(AssertPath, self).__init__()

    def parse(self, path):
        pass  # TODO: implementation
CommandFactory().add_class(AssertPath.__name__, AssertPath)


# Assertions on Cookie
class AssertCookie(Command):
    def __init__(self):
        super(AssertCookie, self).__init__()

    def parse(self, path):
        pass  # TODO: implementation
CommandFactory().add_class(AssertCookie.__name__, AssertCookie)


# Base class for testing time
class AssertTime(Command):
    def __init__(self):
        super(AssertTime, self).__init__()

    def parse(self, path):
        new_class_name = self.__class__.__name__ + path[0]

        next_step = eval(new_class_name + "()")
        next_step.parse(path[1:])
CommandFactory().add_class(AssertTime.__name__, AssertTime)


# Test total time of request
class AssertTimeTotal(Command):
    def __init__(self):
        super(AssertTimeTotal, self).__init__()

    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        print("Asserting total request time is {}".format(str(args)))
CommandFactory().add_class(AssertTimeTotal.__name__, AssertTimeTotal)


# Average time per request?
class AssertTimeAverage(Command):
    def __init__(self):
        super(AssertTimeAverage, self).__init__()

    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        print("Asserting average request time is {}".format(str(args)))
CommandFactory().add_class(AssertTimeAverage.__name__, AssertTimeAverage)