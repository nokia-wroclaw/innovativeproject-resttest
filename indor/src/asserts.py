    # coding=utf-8
from requests.structures import CaseInsensitiveDict
from abstract_test import AbstractTest
from result_collector import ResultCollector


# This class inherits from the class Assert
# Base class for Assertion on Response
class AssertResponse(AbstractTest):
    def parse(self, path):
        if len(path) == 0:
            raise Exception("Za mało argumentów")
        if path[0] == "Not" and len(path) < 2:
            raise Exception("Za mało argumentów")

        classes_names = CaseInsensitiveDict()
        classes_names['status'] = 'Status'
        classes_names['empty'] = 'Empty'
        classes_names['length'] = 'Length'
        classes_names['time'] = 'Time'
        classes_names['type'] = 'ContentType'
        classes_names['not'] = 'Not'

        if path[0] == "Not":
            new_class_name = self.__class__.__name__ + classes_names[path[0]] + classes_names[path[1]]
            passed_args = path[2:]
        else:
            new_class_name = self.__class__.__name__ + classes_names[path[0]]
            passed_args = path[1:]

        next_step = eval(new_class_name + "()")
        next_step.parse(passed_args)


class AssertResponseStatus(AbstractTest):
    """
    This class inherits from the class AssertResponse
    In this class we are able to check status of response
    """

    def __init__(self):
        super(AssertResponseStatus, self).__init__()
        self.mapping = {
            "Ok": 200,
            "Not found": 404
        }

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
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        status = args[0]

        if not status.isdigit():
            status = self.map_status_code(status)

        self.result.status = (ResultCollector().get_response().status_code == int(status))
        self.result.expected = status
        self.result.actual = ResultCollector().get_response().status_code


# This class is for check type of content of response
class AssertResponseContentType(AbstractTest):
    def parse(self, path):
        if path[0] == "Json":
            next_step = AssertResponseContentTypeJson()
            next_step.parse([])
        else:
            raise Exception("Bad param")


class AssertResponseContentTypeJson(AbstractTest):
    """Check if content type is JSON"""

    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute()

    def execute(self):
        try:
            ResultCollector().get_response().json()
        except ValueError, e:
            self.result.status = False
        else:
            self.result.status = True


# This class is for check length of response
class AssertResponseLength(AbstractTest):
    def parse(self, path):
        # assert 'content-length' in TestRunner.response.headers
        # Jeśli 'transfer-encoding' == 'chunked' wtedy nie ma headea content-length

        if path[0] == ">":
            next_step = AssertResponseLengthGreater()
            next_step.parse(path[1])
        else:
            raise Exception("Bad param or not implemented yet")
            # TODO: implementation


class AssertResponseLengthGreater(AbstractTest):
    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        if 'content-length' in ResultCollector().get_response().headers:
            self.result.status = (int(ResultCollector().get_response().headers['content-length']) > int(args))
            self.result.actual = ResultCollector().get_response().headers['content-length']
        else:
            self.result.status = (len(ResultCollector().get_response().content) > int(args))
            self.result.actual = len(ResultCollector().get_response().content)
        self.result.expected = "> " + args


# Is response empty?
class AssertResponseEmpty(AbstractTest):
    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        self.result.status = (ResultCollector().get_response().content == "")
        self.result.actual = ResultCollector().get_response().content


# Is response NOT empty?
class AssertResponseNotEmpty(AbstractTest):
    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute()

    def execute(self):
        self.result.status = (ResultCollector().get_response().content != "")
        self.result.actual = ResultCollector().get_response().content


# Check Time of Response
class AssertResponseTime(AbstractTest):
    def __init__(self):
        super().__init__()

    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        raise Exception("Not implemented yet")


# ??
class AssertPath(AbstractTest):
    def __init__(self):
        super().__init__()

    def parse(self, path):
        pass  # TODO: implementation


# Assertions on Cookie
class AssertCookie(AbstractTest):
    def __init__(self):
        super().__init__()

    def parse(self, path):
        pass  # TODO: implementation


# Base class for testing time
class AssertTime(AbstractTest):
    def __init__(self):
        super().__init__()

    def parse(self, path):
        new_class_name = self.__class__.__name__ + path[0]

        next_step = eval(new_class_name + "()")
        next_step.parse(path[1:])


# Test total time of request
class AssertTimeTotal(AbstractTest):
    def __init__(self):
        super().__init__()

    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        print("Asserting total request time is {}".format(str(args)))


# Average time per request?
class AssertTimeAverage(AbstractTest):
    def __init__(self):
        super().__init__()

    def parse(self, path):
        ResultCollector().add_result(self)
        self.execute(path)

    def execute(self, args):
        print("Asserting average request time is {}".format(str(args)))
