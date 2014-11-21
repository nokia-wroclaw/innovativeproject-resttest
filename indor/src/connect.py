from abstract_test import AbstractTest
from result_collector import ResultCollector
import requests

PARAMS_NAME = "PARAMS"
HEADERS_NAME = "HEADERS"
AUTH_NAME = "AUTH"


def find_keywords_begin_and_end(path, text):
    """

    :param path:
    :type path: str
    :param text:
    :type text: str
    :return: (begin, end)
    :rtype: list
    """
    begin = path.find("%s" % text)

    if begin == -1:
        return 0, 0

    begin = begin + len(text) + 1
    end = path.find(",", begin)
    return begin, end


class Connect(AbstractTest):
    """Make request"""

    def __init__(self):
        self.params = {}
        self.headers = {}
        self.url = ""
        self.arguments = ""

    def parse_params(self, path):
        begin, end = find_keywords_begin_and_end(path, PARAMS_NAME)

        if end > 0:
            splitted = path[begin: end].split(" ")
        else:
            splitted = path[begin:].split(" ")

        for i in range(0, len(splitted) / 2):
            self.params[splitted[2 * i]] = splitted[2 * i + 1]

    def parse_headers(self, path):
        begin, end = find_keywords_begin_and_end(path, HEADERS_NAME)

        if end > 0:
            splitted = path[begin: end].split(" ")
        else:
            splitted = path[begin:].split(" ")

        for i in range(0, len(splitted) / 2):
            self.headers[splitted[2 * i]] = splitted[2 * i + 1]

    def parse_url(self, path):
        args = path.split(" ")
        self.url = args[0].strip(",")

    def get_auth(self):
        begin, end = find_keywords_begin_and_end(self.arguments, AUTH_NAME)

        if end > 0:
            splitted = self.arguments[begin: end].split(" ")
        else:
            splitted = self.arguments[begin:].split(" ")

        if len(splitted) == 2: #only username and password -> we assume that it is basic auth
            return requests.auth.HTTPBasicAuth(splitted[0], splitted[1])
        return []

    def parse(self, path):
        argument = path[0]

        arguments = " ".join(path[1:])
        self.arguments = arguments

        self.parse_params(arguments)
        self.parse_headers(arguments)
        self.parse_url(arguments)

        try:
            func = getattr(requests, argument.lower())
        except AttributeError:
            print('function not found "%s"' % (argument.lower()))
        else:
            ResultCollector().set_response(func(url=self.url, params=self.params, auth=self.get_auth()))