# coding=utf-8
from requests.structures import CaseInsensitiveDict
from requests.status_codes import codes, _codes

from command import Command
from command_factory import CommandFactory
from command_register import CommandRegister
from parsed_value import ParsedValue
from parsing_exception import ParsingException
from result import Error, Passed, Failed
from indor_exceptions import InvalidRelationalOperator, KeywordNotFound, SyntaxErrorWrongNumberOfArguments
import result
from relational_operators import compare_by_supposed_relational_operator


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
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         'At least two arguments expected: relational operator and number. Example: < 2')

        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        try:
            relational_operator = args[0]
            expected = int(args[1])

            actual = len(response.history)

            if compare_by_supposed_relational_operator(actual, relational_operator, expected):
                self.result_collector.add_result(Passed(self))
            else:
                self.result_collector.add_result(Failed(self, relational_operator + " " + args[1], str(actual)))
        except ValueError:
            self.result_collector.add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
        except InvalidRelationalOperator as e:
            self.result_collector.add_result(Error.from_exception(self, e))


class AssertResponse(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE"

    def __init__(self, result_collector):
        super(AssertResponse, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        next_step.parse(path[1:])


class AssertResponseNot(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE NOT"

    def __init__(self, result_collector):
        super(AssertResponseNot, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

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

        if status not in self.mapping:
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
                self.result_collector.add_result(Error.from_exception(self, e))
                return
        else:
            if int(status) not in _codes.keys():
                self.result_collector.add_result(Error(self, result.ERROR_INVALID_STATUS_CODE,
                                                       "Got " + status + " but only " + _codes.keys().__str__() + " is valid."))
                return

        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        actual = response.status_code
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
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

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
        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        try:
            response.json()
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
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         'At least two arguments expected: relational operator and number. Example: < 2')

        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        try:
            relational_operator = args[0]
            expected = int(args[1])

            content_length = len(response.content)

            if compare_by_supposed_relational_operator(content_length, relational_operator, expected):
                self.result_collector.add_result(Passed(self))
            else:
                self.result_collector.add_result(Failed(self, relational_operator + " " + args[1], content_length))
        except ValueError:
            self.result_collector.add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
        except InvalidRelationalOperator as e:
            self.result_collector.add_result(Error.from_exception(self, e))


class AssertResponseEmpty(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE EMPTY"

    def __init__(self, result_collector):
        super(AssertResponseEmpty, self).__init__(result_collector)

    def parse(self, path):
        self.execute()

    def execute(self):
        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        if len(response.content) != 0:
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
        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        if len(response.content) == 0:
            self.result_collector.add_result(Failed(self, "`NOT EMPTY`", "`EMPTY`"))
        else:
            self.result_collector.add_result(Passed(self))


class AssertResponseTime(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE TIME"

    def __init__(self, result_collector):
        super(AssertResponseTime, self).__init__(result_collector)

    def parse(self, path):
        self.execute(path)

    def execute(self, args):
        if len(args) < 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         'At least two arguments expected: relational operator and number. Example: < 2')

        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        try:
            relational_operator = args[0]
            expected = int(args[1])

            response_time = response.elapsed.total_seconds() * 1000

            if compare_by_supposed_relational_operator(response_time, relational_operator, expected):
                self.result_collector.add_result(Passed(self))
            else:
                self.result_collector.add_result(Failed(self, relational_operator + " " + args[1], response_time))
        except ValueError:
            self.result_collector.add_result(Error(self, result.ERROR_NUMBER_EXPECTED))
        except InvalidRelationalOperator as e:
            self.result_collector.add_result(Error.from_exception(self, e))


class CommandCookie(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT COOKIE"

    def __init__(self, result_collector):
        super(CommandCookie, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


class CommandCookieSet(Command):
    __metaclass__ = CommandRegister

    pretty_name = "COOKIE SET"

    def __init__(self, result_collector):
        super(CommandCookieSet, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__)

        return self.execute(path)

    def execute(self, path):
        cookie_name = path[0]

        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        computed = cookie_name in response.cookies
        parsed = ParsedValue(self, True, "'" + cookie_name + "' cookie in " + [cookie.name for cookie in
                                                                               response.cookies].__str__())
        return computed, parsed


class CommandCookieValue(Command):
    __metaclass__ = CommandRegister

    pretty_name = "COOKIE VALUE"

    def __init__(self, result_collector):
        super(CommandCookieValue, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'Two arguments expected: cookie name and cookie value.')

        return self.execute(path)

    def execute(self, path):
        cookie_name = path[0]
        expected_cookie_value = path[1]

        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        if cookie_name not in response.cookies:
            raise ParsingException(self, "cookie '" + cookie_name + "' not found")

        return response.cookies[cookie_name], ParsedValue(self, expected_cookie_value, "")


class AssertHeader(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT HEADER"

    def __init__(self, result_collector):
        super(AssertHeader, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        next_step.parse(path[1:])


class AssertHeaderSet(Command):
    __metaclass__ = CommandRegister

    pretty_name = "HEADER SET"

    def __init__(self, result_collector):
        super(AssertHeaderSet, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 1:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'One argument expected: header name.')

        self.execute(path)

    def execute(self, path):
        header_name = path[0]

        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        headers = response.headers

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
        if len(path) != 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'Two arguments expected: header name and header value.')

        self.execute(path)

    def execute(self, path):
        header_name = path[0]
        expected_header_value = path[1]

        response = self.result_collector.get_response()

        if response is None:
            self.result_collector.add_result(Error(self, result.ERROR_RESPONSE_NOT_FOUND))
            return

        actual_header_value = response.headers.get(header_name)

        if actual_header_value is None:
            self.result_collector.add_result(Error(self, "header '" + header_name + "' not found"))
            return

        if expected_header_value == actual_header_value:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, expected_header_value, actual_header_value))


class CommandText(Command):
    __metaclass__ = CommandRegister

    pretty_name = "TEXT"

    def __init__(self, result_collector):
        super(CommandText, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            response = self.result_collector.get_response()
            if response is None:
                raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)
            return response.text, ParsedValue(self, None, "")

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


class CommandTextContains(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT TEXT CONTAINS"

    def __init__(self, result_collector):
        super(CommandTextContains, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'At least one argument expected')

        return self.execute(path)

    def execute(self, path):
        response = self.result_collector.get_response()

        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        needle = ' '.join(path)
        haystack = response.text

        computed = needle in haystack
        parsed = ParsedValue(self, True, needle + " IS CONTAINED")
        return computed, parsed
