__author__ = 'Bartosz Zieba'


# Base class for all tests
class Test:
    request = None
    list_of_test_class = []  # list of all class created in this test

    def __init__(self):
        Test.list_of_test_class = []
        Test.request = None


# Base class for all conection
class Connect(Test):
    # path - definition of test class
    def __init__(self, path=""):
        if self.parse(path):
            Connect.list_of_test_class.append(self)

    #TODO: class tree parser
    def parse(self, path):
        return True


# Class for send GET request
class ConnectGET(Connect):
    def __init__(self, path=""):
        if self.parse(path):
            ConnectGET.list_of_test_class.append(self)

    #TODO: class tree parser
    def parse(self, path):
        return True


# Class for send POST request
class ConnectPOST(Connect):
    def __init__(self, path=""):
        if self.parse(path):
            ConnectPOST.list_of_test_class.append(self)

    #TODO: class tree parser
    def parse(self, path):
        return True


# Class for send PUT request
class ConnectPUT(Connect):
    def __init__(self, path=""):
        if self.parse(path):
            ConnectPUT.list_of_test_class.append(self)

    #TODO: class tree parser
    def parse(self, path):
        return True


# This class inherits from the class Test
# Base class for Assertions
class Assert(Test):
    def __init__(self, path=""):
        if self.parse(path):
            Assert.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# This class inherits from the class Assert
# Base class for Assertion on Response
class AssertResponse(Assert):
    def __init__(self, path=""):
        if self.parse(path):
            AssertResponse.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# This class inherits from the class AssertResponse
# In this class we able to check status of response
class AssertResponseStatus(AssertResponse):
    def __init__(self, path=""):
        if self.parse(path):
            AssertResponseStatus.list_of_test_class.append(self)
            self.code = self.get_code_from_request()

    #TODO: Assert class tree parser
    def parse(self, path):
        return True

    #TODO: Parse status code from response
    def get_code_from_request(self):
        return 1

    # TODO: check code
    def status_code_is(self, code):
        return True

# This class is for check type of content of response
class AssertResponseContentType(AssertResponse):
    def __init__(self, path=""):
        if self.parse(path):
            AssertResponseContentType.list_of_test_class.append(self)
            self.content_type = self.get_content_type_from_response()

    #TODO: Assert class tree parser
    def parse(self, path):
        return True

    #TODO: Parse data type from response
    def get_content_type_from_response(self):
        return "XML"

    #TODO: Check type
    def content_type_is(self, type):
        return True


# This class is for check length of response
class AssertResponseLength(AssertResponse):
    def __init__(self, path=""):
        if self.parse(path):
            AssertResponseLength.list_of_test_class.append(self)
            self.length = self.length_of_response()

    #TODO: Assert class tree parser
    def parse(self, path):
        return True

    #TODO: return length of response
    def length_of_response(self):
        return 0


# Is response smpty?
class AssertResponseEmpty(AssertResponse):
    def __init__(self, path=""):
        if self.parse(path):
            AssertResponseEmpty.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# Is response NOT empty?
class AssertResponseNotEmpty(AssertResponse):
    def __init__(self, path=""):
        if self.parse(path):
            AssertResponseEmpty.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# Check Time of Response
class AssertResponseTime(AssertResponse):
    def __init__(self, path=""):
        if self.parse(path):
            AssertResponseTime.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# ??
class AssertPath(Assert):
    def __init__(self, path=""):
        if self.parse(path):
            AssertPath.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# Assertions on Coockie
class AssertCookie(Assert):
    def __init__(self, path=""):
        if self.parse(path):
            AssertCookie.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# Base class for testing time
class AssertTime(Assert):
    def __init__(self, path=""):
        if self.parse(path):
            AssertTime.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# Test total time of request
class AssertTimeTotal(AssertTime):
    def __init__(self, path=""):
        if self.parse(path):
            AssertTimeTotal.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True


# Average time per request?
class AssertTimeAverage(AssertTime):
    def __init__(self, path=""):
        if self.parse(path):
            AssertTimeAverage.list_of_test_class.append(self)

    #TODO: Assert class tree parser
    def parse(self, path):
        return True
