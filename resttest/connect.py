from abstract_test import AbstractTest
from result_collector import ResultCollector
import requests
PARAMS_NAME = "PARAMS"
HEADERS_NAME = "HEADERS"


class Connect(AbstractTest):
    """Make request"""

    def __init__(self):
        self.params = {}
        self.headers = {}
        self.url = ""

    def parse_params(self, path):
        begin = path.find("%s" % PARAMS_NAME) + 7
        end = path.find(",", begin)

        if end > 0:
            splitted = path[begin: end].split(" ")
        else:
            splitted = path[begin:].split(" ")

        for i in range(0, len(splitted) / 2):
            self.params[splitted[2 * i]] = splitted[2 * i + 1]

    def parse_headers(self, path):
        begin = path.find("%s" % HEADERS_NAME) + 8
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
            print('function not found "%s"' % (argument.lower()))
        else:
            ResultCollector().set_response(func(url=self.url, params=self.params))