# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławuś Domagała'


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
            print "\t {}: status {}, message {}".format(test.__class__.__name__, test.status, test.message)

    def run_test(self, test_lines):
        for line in test_lines:
            test = Test()
            args = line.strip(".").split(" ")
            test.parse(args)

        self.print_summary()


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


# Base class for all conections
class Connect(Test):
    # path - definition of test class
    def __init__(self):
        self.params = {}
        self.headers = {}
        self.url = ""


    def parseParams(self, path):
        begin = path.find("PARAMS") + 7
        end = path.find(",", begin)

        if (end > 0):
            splitted = path[begin: end].split(" ")
        else:
            splitted = path[begin:].split(" ")

        for i in range(0, len(splitted) / 2):
            self.params[splitted[2 * i]] = splitted[2 * i + 1]

    def parseHeaders(self, path):
        begin = path.find("HEADERS") + 8
        end = path.find(",", begin)

        if (end > 0):
            splitted = path[begin: end].split(" ")
        else:
            splitted = path[begin:].split(" ")

        for i in range(0, len(splitted) / 2):
            self.headers[splitted[2 * i]] = splitted[2 * i + 1]

    def parseUrl(self, path):
        args = path.split(" ")
        self.url = args[0].strip(",")

    def parse(self, path):
        argument = path[0]

        if argument == 'GET':
            next_step = ConnectGET()
        elif argument == 'POST':
            next_step = ConnectPOST()
        elif argument == 'PUT':
            next_step = ConnectPUT()
        elif argument == 'DELETE':
            next_step = ConnectDELETE()

        next_step.parse(path[1:])


# Class for sending GET request
class ConnectGET(Connect):
    def __init__(self):
        Connect.__init__(self)

    def execute(self, arguments):
        # TODO: Damian - do your job here
        self.parseParams(arguments)
        self.parseHeaders(arguments)
        self.parseUrl(arguments)

        print "GET to {} with params: {}".format(self.url, str(self.params))  # TODO: delete it

    def parse(self, path):
        joined_path = " ".join(path)
        self.execute(joined_path)


# Class for sending POST request
class ConnectPOST(Connect):
    def __init__(self):
        Connect.__init__(self)

    def execute(self, arguments):
        # TODO: Damian - do your job here
        self.parseParams(arguments)
        self.parseHeaders(arguments)
        self.parseUrl(arguments)

        print "POST to {} with params: {}".format(self.url, str(self.params))  # TODO: delete it

    def parse(self, path):
        joined_path = " ".join(path)
        self.execute(joined_path)\


# Class for sending PUT request
class ConnectPUT(Connect):
    def __init__(self):
        Connect.__init__(self)

    def execute(self, arguments):
        # TODO: Damian - do your job here
        self.parseParams(arguments)
        self.parseHeaders(arguments)
        self.parseUrl(arguments)

    def parse(self, path):
        joined_path = " ".join(path)
        self.execute(joined_path)\


# Class for sending DELETE request
class ConnectDELETE(Connect):
    def __init__(self):
        Connect.__init__(self)

    def execute(self, arguments):
        # TODO: Damian - do your job here
        self.parseParams(arguments)
        self.parseHeaders(arguments)
        self.parseUrl(arguments)

    def parse(self, path):
        joined_path = " ".join(path)
        self.execute(joined_path)\


# This class inherits from the class Test
# Base class for Assertions
class Assert(Test):
    def __init__(self):
        self.status = 0
        self.message = ":D"

    def parse(self, path):
        # Convert all arguments to CamelCase
        arguments = map(lambda x: x.title(), path)

        new_class_name = self.__class__.__name__ + arguments[0]

        next_step = eval(new_class_name + "()")
        next_step.parse(arguments[1:])


# This class inherits from the class Assert
# Base class for Assertion on Response
class AssertResponse(Assert):
    def __init__(self):
        pass

    def parse(self, path):
        argument = path[0]
        argument2 = " ".join(path[0:2])

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


# This class inherits from the class AssertResponse
# In this class we are able to check status of response
class AssertResponseStatus(AssertResponse):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        print "Asserting status is {}".format(args[0])


# This class is for check type of content of response
class AssertResponseContentType(AssertResponse):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        print "Asserting content type is {}".format(args[0])


# This class is for check length of response
class AssertResponseLength(AssertResponse):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        print "Asserting response length is {}".format(str(args))


# Is response empty?
class AssertResponseEmpty(AssertResponse):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        print "Asserting response length is empty"


# Is response NOT empty?
class AssertResponseNotEmpty(AssertResponse):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        print "Asserting response length is not empty"


# Check Time of Response
class AssertResponseTime(AssertResponse):
    def __init__(self):
        Assert.__init__(self)

    def parse(self, path):
        TestRunner.list_of_test_classes.append(self)
        self.execute(path)

    def execute(self, args):
        print "Asserting response time is {}".format(str(args))


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
