# coding=utf-8
from command import Command
from command_factory import CommandFactory
from command_register import CommandRegister
from result import Error, Passed, Failed
from indor_exceptions import InvalidRelationalOperator, KeywordNotFound
import result
from requests.structures import CaseInsensitiveDict
from assert_path import AssertPath


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
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE REDIRECTS"

    def __init__(self, result_collector):
        super(AssertResponseRedirects, self).__init__(result_collector)

    def parse(self, path):
        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        next_step.parse(path[1:])


class AssertResponseRedirectsCount(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE REDIRECTS COUNT"

    def __init__(self, result_collector):
        super(AssertResponseRedirectsCount, self).__init__(result_collector)

    def parse(self, path):
        self.execute(path)

    def execute(self, args):
        if len(args) < 2:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        try:
            relational_operator = extract_relational_operator(args[0])
            expected = int(args[1])
        except ValueError:
            self.result_collector.add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
            return
        except InvalidRelationalOperator as e:
            self.result_collector.add_result(Error(self, e.message))
            return

        actual = len(self.result_collector.get_response().history)

        if compare_by_relational_operator(actual, relational_operator, expected):
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, relational_operator + " " + args[1], str(actual)))


class AssertResponse(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE"

    def __init__(self, result_collector):
        super(AssertResponse, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        if next_step is None:
            self.result_collector.add_result(Error(self, KeywordNotFound(path[0])))
            return

        next_step.parse(path[1:])


class AssertResponseNot(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE NOT"

    def __init__(self, result_collector):
        super(AssertResponseNot, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        next_step.parse(path[1:])


class AssertResponseStatus(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE STATUS"

    def __init__(self, result_collector):
        super(AssertResponseStatus, self).__init__(result_collector)
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
                self.result_collector.add_result(Error(self, e))
                return

        actual = self.result_collector.get_response().status_code
        expected = int(status)
        if actual == expected:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, expected, actual))


class AssertResponseType(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE TYPE"

    def __init__(self, result_collector):
        super(AssertResponseType, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        next_step.parse(path[1:])


class AssertResponseTypeJson(Command):
    __metaclass__ = CommandRegister
    pretty_name = "RESPONSE CONTENT TYPE IS JSON"

    def __init__(self, result_collector):
        super(AssertResponseTypeJson, self).__init__(result_collector)

    def parse(self, path):
        self.execute()

    def execute(self):
        try:
            self.result_collector.get_response().json()
        except ValueError:
            self.result_collector.add_result(Failed(self, "json", "not json"))
        else:
            self.result_collector.add_result(Passed(self))


class AssertResponseLength(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE LENGTH"

    def __init__(self, result_collector):
        super(AssertResponseLength, self).__init__(result_collector)

    def parse(self, path):
        self.execute(path)

    def execute(self, args):
        if len(args) < 2:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        try:
            relational_operator = extract_relational_operator(args[0])
            expected = int(args[1])
        except ValueError:
            self.result_collector.add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
            return
        except InvalidRelationalOperator as e:
            self.result_collector.add_result(Error(self, e.message))
            return

        if 'content-length' in self.result_collector.get_response().headers:
            content_length = int(self.result_collector.get_response().headers['content-length'])
        else:
            content_length = len(self.result_collector.get_response().content)

        if content_length > expected:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, relational_operator + " " + args[1], content_length))


class AssertResponseEmpty(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE EMPTY"

    def __init__(self, result_collector):
        super(AssertResponseEmpty, self).__init__(result_collector)

    def parse(self, path):
        self.execute()

    def execute(self):
        if len(self.result_collector.get_response().content) != 0:
            self.result_collector.add_result(Failed(self, "`EMPTY`", "`NOT EMPTY`"))
        else:
            self.result_collector.add_result(Passed(self))


class AssertResponseNotEmpty(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE NOT EMPTY"

    def __init__(self, result_collector):
        super(AssertResponseNotEmpty, self).__init__(result_collector)

    def parse(self, path):
        self.execute()

    def execute(self):
        if len(self.result_collector.get_response().content) == 0:
            self.result_collector.add_result(Failed(self, "`NOT EMPTY`", "`EMPTY`"))
        else:
            self.result_collector.add_result(Passed(self))


class AssertResponseTime(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE TIME"

    def __init__(self, result_collector):
        super(AssertResponseTime, self).__init__(result_collector)

    def parse(self, path):
        self.result_collector.add_result(self)
        self.execute(path)

    def execute(self, args):
        raise Exception("Not implemented yet")


class AssertCookie(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT COOKIE"

    def __init__(self, result_collector):
        super(AssertCookie, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        next_step.parse(path[1:])


class AssertCookieSet(Command):
    __metaclass__ = CommandRegister

    pretty_name = "COOKIE SET"

    def __init__(self, result_collector):
        super(AssertCookieSet, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        self.execute(path)

    def execute(self, path):
        cookie_name = path[0]
        try:
            self.result_collector.get_response().cookies[cookie_name]
            self.result_collector.add_result(Passed(self))
        except KeyError:
            self.result_collector.add_result(Failed(self, "'" + cookie_name + "' cookie set",
                                    [cookie.name for cookie in self.result_collector.get_response().cookies].__str__()))


class AssertCookieValue(Command):
    __metaclass__ = CommandRegister

    pretty_name = "COOKIE VALUE"

    def __init__(self, result_collector):
        super(AssertCookieValue, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        self.execute(path)

    def execute(self, path):
        cookie_name = path[0]
        expected_cookie_value = path[1]

        try:
            actual_cookie_value = self.result_collector.get_response().cookies[cookie_name]
        except KeyError:
            self.result_collector.add_result(Error(self, "cookie '" + cookie_name + "' not found"))
            return

        if expected_cookie_value == actual_cookie_value:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, expected_cookie_value, actual_cookie_value))


class AssertHeader(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT HEADER"

    def __init__(self, result_collector):
        super(AssertHeader, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        next_step.parse(path[1:])


class AssertHeaderSet(Command):
    __metaclass__ = CommandRegister

    pretty_name = "HEADER SET"

    def __init__(self, result_collector):
        super(AssertHeaderSet, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        self.execute(path)

    def execute(self, path):
        header_name = path[0]

        headers = self.result_collector.get_response().headers

        if headers.get(header_name):
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, "'" + header_name + "' header set", headers.keys().__str__()))


class AssertHeaderValue(Command):
    __metaclass__ = CommandRegister

    pretty_name = "HEADER VALUE"

    def __init__(self, result_collector):
        super(AssertHeaderValue, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        self.execute(path)

    def execute(self, path):
        header_name = path[0]
        expected_header_value = path[1]

        actual_header_value = self.result_collector.get_response().headers.get(header_name)

        if actual_header_value is None:
            self.result_collector.add_result(Error(self, "header '" + header_name + "' not found"))
            return

        if expected_header_value == actual_header_value:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, expected_header_value, actual_header_value))


class AssertText(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT TEXT"

    def __init__(self, result_collector):
        super(AssertText, self).__init__(result_collector)

    def parse(self, path):
        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        next_step.parse(path[1:])


class AssertTextContains(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT TEXT CONTAINS"

    def __init__(self, result_collector):
        super(AssertTextContains, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
            return

        self.execute(path)

    def execute(self, path):
        needle = ' '.join(path)
        haystack = self.result_collector.get_response().text

        if needle in haystack:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, needle + " not found", ""))



# Base class for testing time
class AssertTime(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT TIME"

    def __init__(self, result_collector):
        super(AssertTime, self).__init__(result_collector)

    def parse(self, path):
        new_class_name = self.__class__.__name__ + path[0]

        next_step = eval(new_class_name + "()")
        next_step.parse(path[1:])


# Test total time of request
class AssertTimeTotal(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT TIME TOTAL"

    def __init__(self, result_collector):
        super(AssertTimeTotal, self).__init__(result_collector)

    def parse(self, path):
        self.result_collector.add_result(self)
        self.execute(path)

    def execute(self, args):
        print("Asserting total request time is {}".format(str(args)))


# Average time per request?
class AssertTimeAverage(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT TIME AVERAGE"

    def __init__(self, result_collector):
        super(AssertTimeAverage, self).__init__(result_collector)

    def parse(self, path):
        self.result_collector.add_result(self)
        self.execute(path)

    def execute(self, args):
        print("Asserting average request time is {}".format(str(args)))
