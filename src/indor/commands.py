from .command import Command
from .command_factory import CommandFactory
from .command_register import CommandRegister
from .parsed_value import ParsedValue
from .parsing_exception import ParsingException
from .result import Error, Passed, Failed
from .indor_exceptions import SyntaxErrorWrongNumberOfArguments
from . import result


class CommandCookie(Command, metaclass=CommandRegister):
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


class CommandCookieSet(Command, metaclass=CommandRegister):
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


class CommandCookieValue(Command, metaclass=CommandRegister):
    pretty_name = "COOKIE VALUE"

    def __init__(self, result_collector):
        super(CommandCookieValue, self).__init__(result_collector)

    def parse(self, path):
        return self.execute(path)

    def execute(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'Too few arguments expected: cookie name and cookie value.')

        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        cookie_name = path[0]

        if cookie_name not in response.cookies:
            raise ParsingException(self, "cookie '" + cookie_name + "' not found")

        if len(path) == 1:
            return response.cookies[cookie_name], ParsedValue(self, None, "")

        expected_cookie_value = path[1]

        return response.cookies[cookie_name], ParsedValue(self, expected_cookie_value, "")


class CommandHeader(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT HEADER"

    def __init__(self, result_collector):
        super(CommandHeader, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


class CommandHeaderSet(Command, metaclass=CommandRegister):
    pretty_name = "HEADER SET"

    def __init__(self, result_collector):
        super(CommandHeaderSet, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 1:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'One argument expected: header name.')

        self.execute(path)

    def execute(self, path):
        header_name = path[0]

        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        headers = response.headers

        computed = header_name in headers
        parsed = ParsedValue(self, True, "'" + header_name + "' header in " + headers.keys().__str__())
        return computed, parsed


class CommandHeaderValue(Command, metaclass=CommandRegister):
    pretty_name = "HEADER VALUE"

    def __init__(self, result_collector):
        super(CommandHeaderValue, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 1 or len(path) > 2:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__, 'Two arguments expected: header name and header value.')

        return self.execute(path)

    def execute(self, path):
        header_name = path[0]

        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        actual_header_value = response.headers.get(header_name)

        if actual_header_value is None:
            raise ParsingException(self, "header '" + header_name + "' not found")

        if len(path) == 1:
            return actual_header_value, ParsedValue(self, None, "")

        expected_header_value = path[1]

        return actual_header_value, ParsedValue(self, expected_header_value, "")


class CommandText(Command, metaclass=CommandRegister):
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


class CommandTextContains(Command, metaclass=CommandRegister):
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
