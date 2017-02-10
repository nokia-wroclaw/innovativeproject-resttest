from requests.status_codes import _codes
from requests.structures import CaseInsensitiveDict
from .command import Command
from .command_factory import CommandFactory
from .command_register import CommandRegister
from .indor_exceptions import SyntaxErrorWrongNumberOfArguments, InvalidRelationalOperator
from .parsed_value import ParsedValue
from .parsing_exception import ParsingException
from .relational_operators import compare_by_supposed_relational_operator
from .result import Error, Passed, Failed
from . import result


class CommandResponseRedirects(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT RESPONSE REDIRECTS"

    def __init__(self, result_collector):
        super(CommandResponseRedirects, self).__init__(result_collector)

    def parse(self, path):
        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


class CommandResponseRedirectsCount(Command, metaclass=CommandRegister):
    pretty_name = "RESPONSE REDIRECTS COUNT"

    def __init__(self, result_collector):
        super(CommandResponseRedirectsCount, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 2 and len(path) != 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         'Two or zero arguments expected: relational operator and number. Example: < 2')

        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        try:
            actual = len(response.history)

            if len(path) == 0:
                actual, ParsedValue(self, None, "")

            relational_operator = path[0]
            expected = int(path[1])

            parsed = ParsedValue(self, True, relational_operator + " " + path[1])
            computed = compare_by_supposed_relational_operator(actual, relational_operator, expected)
            return computed, parsed
        except ValueError:
            raise ParsingException(self, result.ERROR_NUMBER_EXPECTED)
        except InvalidRelationalOperator as e:
            raise ParsingException(self, Error.from_exception(self, e))


class CommandResponse(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT RESPONSE"

    def __init__(self, result_collector):
        super(CommandResponse, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


class CommandResponseNot(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT RESPONSE NOT"

    def __init__(self, result_collector):
        super(CommandResponseNot, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


class CommandResponseStatus(Command, metaclass=CommandRegister):
    pretty_name = "RESPONSE STATUS"

    def __init__(self, result_collector):
        super(CommandResponseStatus, self).__init__(result_collector)
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
        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        actual = response.status_code

        if len(path) == 0:
            return actual, ParsedValue(self, None, "")

        status = path[0]

        if not status.isdigit():
            try:
                status = self.map_status_code(status)
            except LookupError as e:
                raise ParsingException(self, Error.from_exception(self, e))
        else:
            if int(status) not in _codes.keys():
                raise ParsingException(self, result.ERROR_INVALID_STATUS_CODE)

        expected = int(status)
        return actual, ParsedValue(self, expected, "")


class CommandResponseType(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT RESPONSE TYPE"

    def __init__(self, result_collector):
        super(CommandResponseType, self).__init__(result_collector)

    def parse(self, path):
        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))

        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


class CommandResponseTypeJson(Command, metaclass=CommandRegister):
    pretty_name = "RESPONSE CONTENT TYPE IS JSON"

    def __init__(self, result_collector):
        super(CommandResponseTypeJson, self).__init__(result_collector)

    def parse(self, path):
        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        try:
            response.json()
        except ValueError:
            return False, ParsedValue(self, True, "not json")
        else:
            return True, ParsedValue(self, True, "not json")


class CommandResponseLength(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT RESPONSE LENGTH"

    def __init__(self, result_collector):
        super(CommandResponseLength, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 2 and len(path) != 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         'Two or zero arguments expected: relational operator and number. Example: < 2')

        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        try:
            content_length = len(response.content)

            if len(path) == 0:
                return content_length, ParsedValue(self, None, "")

            relational_operator = path[0]
            expected = int(path[1])

            parsed = ParsedValue(self, True, relational_operator + " " + path[1])
            computed = compare_by_supposed_relational_operator(content_length, relational_operator, expected)
            return computed, parsed
        except ValueError:
            raise ParsingException(self, result.ERROR_NUMBER_EXPECTED)
        except InvalidRelationalOperator as e:
            raise ParsingException(self, Error.from_exception(self, e))


class CommandResponseEmpty(Command, metaclass=CommandRegister):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE EMPTY"

    def __init__(self, result_collector):
        super(CommandResponseEmpty, self).__init__(result_collector)

    def parse(self, path):
        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        computed = len(response.content) == 0
        parsed = ParsedValue(self, True, "EMPTY")
        return computed, parsed


class CommandResponseNotEmpty(Command, metaclass=CommandRegister):
    pretty_name = "RESPONSE NOT EMPTY"

    def __init__(self, result_collector):
        super(CommandResponseNotEmpty, self).__init__(result_collector)

    def parse(self, args):
        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        computed = len(response.content) != 0
        parsed = ParsedValue(self, True, "NOT EMPTY")
        return computed, parsed


class CommandResponseTime(Command, metaclass=CommandRegister):
    pretty_name = "ASSERT RESPONSE TIME"

    missed_arguments = 'At least two arguments expected: relational operator and number. Example: < 2'

    def __init__(self, result_collector):
        super(CommandResponseTime, self).__init__(result_collector)

    def parse(self, path):
        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        response_time = response.elapsed.total_seconds() * 1000

        if len(path) < 2:
            return response_time, ParsedValue(self, None, "")

        try:
            relational_operator = path[0]
            expected = int(path[1])
            parsed = ParsedValue(self, True, relational_operator + " " + path[1])
            computed = compare_by_supposed_relational_operator(response_time, relational_operator, expected)
            return computed, parsed
        except ValueError:
            raise ParsingException(self, result.ERROR_NUMBER_EXPECTED)
        except InvalidRelationalOperator as e:
            raise ParsingException(self, Error.from_exception(self, e))