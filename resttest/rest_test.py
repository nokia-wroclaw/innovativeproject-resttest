__author__ = 'Bartosz Zieba'


# Base class for all tests
class Test:
    request = None
    list_of_test_class = [] # list of all class created in this test

    def __init__(self):
        Test.list_of_test_class = []
        Test.request = None


class Connect(Test):
    def __init__(self):
        Connect.list_of_test_class.append(self)


class ConnectGET(Connect):
    def __init__(self):
        ConnectGET.list_of_test_class.append(self)


class ConnectPOST(Connect):
    def __init__(self):
        ConnectPOST.list_of_test_class.append(self)


class ConnectPUT(Connect):
    def __init__(self):
        ConnectPUT.list_of_test_class.append(self)






# This class inherits from the class Test
# Base class for Assertions
class Assert(Test):
    def __init__(self):
        Assert.list_of_test_class.append(self)


# This class inherits from the class Assert
# Base class for Assertion on Response
class AssertResponse(Assert):
    def __init__(self):
        AssertResponse.list_of_test_class.append(self)

# This class inherits from the class AssertResponse
# In this class we able to check status of response
class AssertResponseStatus(AssertResponse):
    def __init__(self):
        AssertResponseStatus.list_of_test_class.append(self)
        self.code = self.get_code_from_request()

    #TODO: Parse status code from response
    def get_code_from_request(self):
        return 1

    # TODO: check code
    def status_code_is(self, code):
        return True

# This class is for check type of content of response
class AssertResponseContentType(AssertResponse):
    def __init__(self):
        AssertResponseContentType.list_of_test_class.append(self)
        self.content_type = self.get_content_type_from_response()

    #TODO: Parse data type from response
    def get_content_type_from_response(self):
        return "XML"

    #TODO: Check type
    def type_is(self , type):
        return True

