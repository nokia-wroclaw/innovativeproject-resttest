from requests.status_codes import _codes
from requests.structures import CaseInsensitiveDict
from command import Command
from command_factory import CommandFactory
from command_register import CommandRegister
from indor_exceptions import SyntaxErrorWrongNumberOfArguments, InvalidRelationalOperator
from parsed_value import ParsedValue
from parsing_exception import ParsingException
from relational_operators import compare_by_supposed_relational_operator
from result import Error, Passed, Failed
import result

__author__ = 'Sławomir Domagała'


class CommandResponseRedirects(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE REDIRECTS"

    def __init__(self, result_collector):
        super(CommandResponseRedirects, self).__init__(result_collector)

    def parse(self, path):
        next_step = CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector)
        return next_step.parse(path[1:])


class CommandResponseRedirectsCount(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE REDIRECTS COUNT"

    def __init__(self, result_collector):
        super(CommandResponseRedirectsCount, self).__init__(result_collector)

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


class CommandResponse(Command):
    __metaclass__ = CommandRegister

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


class CommandResponseNot(Command):
    __metaclass__ = CommandRegister

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


class CommandResponseStatus(Command):
    __metaclass__ = CommandRegister

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


class CommandResponseType(Command):
    __metaclass__ = CommandRegister

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


class CommandResponseTypeJson(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE CONTENT TYPE IS JSON"

    def __init__(self, result_collector):
        super(CommandResponseTypeJson, self).__init__(result_collector)

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


class CommandResponseLength(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE LENGTH"

    def __init__(self, result_collector):
        super(CommandResponseLength, self).__init__(result_collector)

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


class CommandResponseEmpty(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE EMPTY"

    def __init__(self, result_collector):
        super(CommandResponseEmpty, self).__init__(result_collector)

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


class CommandResponseNotEmpty(Command):
    __metaclass__ = CommandRegister

    pretty_name = "RESPONSE NOT EMPTY"

    def __init__(self, result_collector):
        super(CommandResponseNotEmpty, self).__init__(result_collector)

    def parse(self, path):
        self.execute()

    def execute(self):
        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        parsed = ParsedValue(self, True, relational_operator + " " + args[1])
            computed = compare_by_supposed_relational_operator(response_time, relational_operator, expected)
            return computed, parsed
        if len(response.content) == 0:
            self.result_collector.add_result(Failed(self, "`NOT EMPTY`", "`EMPTY`"))
        else:
            self.result_collector.add_result(Passed(self))


class CommandResponseTime(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT RESPONSE TIME"

    missed_arguments = 'At least two arguments expected: relational operator and number. Example: < 2'

    def __init__(self, result_collector):
        super(CommandResponseTime, self).__init__(result_collector)

    def parse(self, path):
        self.execute()

    def execute(self, args):
        response = self.result_collector.get_response()
        if response is None:
            raise ParsingException(self, result.ERROR_RESPONSE_NOT_FOUND)

        response_time = response.elapsed.total_seconds() * 1000

        if len(args) < 2:
            return response_time, ParsedValue(self, None, "")

        try:
            relational_operator = args[0]
            expected = int(args[1])
            parsed = ParsedValue(self, True, relational_operator + " " + args[1])
            computed = compare_by_supposed_relational_operator(response_time, relational_operator, expected)
            return computed, parsed
        except ValueError:
            raise ParsingException(self, result.ERROR_NUMBER_EXPECTED)
        except InvalidRelationalOperator as e:
            raise ParsingException(self, Error.from_exception(self, e))