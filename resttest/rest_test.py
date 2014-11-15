# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławuś Domagała'

import requests

class TestRunner:
    response = None
    list_of_test_classes = []  # list of all classes created in this test

    def __init__(self):
        TestRunner.list_of_test_classes = []
        TestRunner.request = None

    def print_summary(self):
        # TODO: Sławek - we need a nice summary here
        print "Tests finished"
        print "Executed tests:"
        for test in TestRunner.list_of_test_classes:
            print "\t {}: status {}, message {}".format(test.__class__.__name__, test.result.status, test.result.message)

    def run_test(self, test_lines):
        for line in test_lines:
            test = Test()
            args = line.strip(".").split(" ")
            test.parse(args)

        self.print_summary()


class Result:
    """Class contains data of any action realized by program."""

    def __init__(self):
        self.status = False
        self.message = ":D"
        self.expected = None
        self.actual = None


# Base class for all tests
class Test:
    def parse(self, path):
        argument = path[0]

        if argument == 'ASSERT':
            next_step = Assert()
            next_step.parse(path[1:])
        elif argument in ['GET', 'POST', 'PUT', 'DELETE']:
            next_step = Connect()
            next_step.parse(path[0:])

        return False


class Connect(Test):
    """Make request"""

    def __init__(self):
        self.params = {}
        self.headers = {}
        self.url = ""

    def parse_params(self, path):
        begin = path.find("PARAMS") + 7
        end = path.find(",", begin)

        if end > 0:
            splitted = path[begin: end].split(" ")
        else:
            splitted = path[begin:].split(" ")

        for i in range(0, len(splitted) / 2):
            self.params[splitted[2 * i]] = splitted[2 * i + 1]

    def parse_headers(self, path):
        begin = path.find("HEADERS") + 8
        end = path.find(",", begin)

        if end > 0:
            splitted = path[begin: end].split(" ")
        else:
            splitted = path[begin:].split(" ")

        for i in range(0, len(splitted) / 2):
            self.headers[splitted[2 * i]] = splitted[2 * i + 1]

    def parse_url(self, path):
        args = path.split(" ")
        self.url = args[0].strip(",")

    def parse(self, path):
        argument = path[0]

        arguments = " ".join(path[1:])
        self.parse_params(arguments)
        self.parse_headers(arguments)
        self.parse_url(arguments)

        try:
            func = getattr(requests, argument.lower())
        except AttributeError:
            print 'function not found "%s"' % (argument.lower())
        else:
            TestRunner.response = func(url=self.url, params=self.params)


# This class inherits from the class Test
# Base class for Assertions
class Assert(Test):
    def __init__(self):
        self.result = Result()

    def parse(self, path):
        # Convert all arguments to CamelCase
        arguments = map(lambda x: x.title(), path)

        new_class_name = self.__class__.__name__ + arguments[0]

        next_step = eval(new_class_name + "()")
        next_step.parse(arguments[1:])


# This class inherits from the class Assert
# Base class for Assertion on Response
class AssertResponse(Assert):

    def parse(self, path):
        argument = path[0]
        argument2 = " ".join(path[0:2])

        # TODO: I think this should be more "generic"?
        if argument2 == 'Not Empty':
            next_step = AssertResponseNotEmpty()
            next_step.parse(path[2:])
        elif argument == 'Status':
            next_step = AssertResponseStatus()
            next_step.parse(path[1:])
        elif argument == 'Empty':
            next_step = AssertResponseEmpty()
            next_step.parse(path[1:])
        elif argument == 'Length':
            next_step = AssertResponseLength()
            next_step.parse(path[1:])
        elif argument == 'Time':
            next_step = AssertResponseTime()
            next_step.parse(path[1:])
        elif argument == 'Type':
            next_step = AssertResponseContentType()
            next_step.parse(path[1:])


class AssertResponseStatus(AssertResponse):
    """
    This class inherits from the class AssertResponse
    In this class we are able to check status of response
    """

    def __init__(self):
        AssertResponse.__init__(self)
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
            raise LookupError("Status" + status + "not found in " + self.mapping.__str__())

        return self.mapping[status]

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        status = args[0]

        if not status.isdigit():
            status = self.map_status_code(status)

        self.result.status = (TestRunner.response.status_code == status)
        self.result.expected = status
        self.result.actual = TestRunner.response.status_code


# This class is for check type of content of response
class AssertResponseContentType(AssertResponse):

    def parse(self, path):
        if path[0] == "Json":
            next_step = AssertResponseContentTypeJson()
            next_step.parse()
        else:
            raise Exception("Bad param")


class AssertResponseContentTypeJson(AssertResponseContentType):
    """Check if content type is JSON"""

    def parse(self):
        TestRunner.list_of_test_classes.append(self)
        self.execute()

    def execute(self):
        try:
            TestRunner.response.json()
        except ValueError, e:
            self.result.status = False
        else:
            self.result.status = True


# This class is for check length of response
class AssertResponseLength(AssertResponse):
    def parse(self, path):
        assert 'content-length' in TestRunner.response.headers

        if path[0] == ">":
            next_step = AssertResponseLengthGreater()
            next_step.parse(path[1])
        else:
            raise Exception("Bad param or not implemented yet")
        # TODO: implementation


class AssertResponseLengthGreater(AssertResponseLength):
    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        self.result.status = (int(TestRunner.response.headers['content-length']) > int(args))
        self.result.expected = ""
        self.result.actual = TestRunner.response.headers['content-length']


# Is response empty?
class AssertResponseEmpty(AssertResponse):

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        self.result.status = (TestRunner.response.content == "")
        self.result.actual = TestRunner.response.content


# Is response NOT empty?
class AssertResponseNotEmpty(AssertResponse):

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute()

    def execute(self):
        self.result.status = (TestRunner.response.content != "")
        self.result.actual = TestRunner.response.content


# Check Time of Response
class AssertResponseTime(AssertResponse):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        raise Exception("Not implemented yet")


# ??
class AssertPath(Assert):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        pass  # TODO: implementation


# Assertions on Cookie
class AssertCookie(Assert):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        pass  # TODO: implementation


# Base class for testing time
class AssertTime(Assert):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        new_class_name = self.__class__.__name__ + path[0]

        next_step = eval(new_class_name + "()")
        next_step.parse(path[1:])


# Test total time of request
class AssertTimeTotal(AssertTime):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        print "Asserting total request time is {}".format(str(args))


# Average time per request?
class AssertTimeAverage(AssertTime):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        print "Asserting average request time is {}".format(str(args))
