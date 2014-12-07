from command import Command
from command_factory import CommandFactory
from command_register import CommandRegister
from result import Error
import indor_exceptions
import requests
import ast
from pyparsing import *

PARAMS_NAME = "PARAMS"
HEADERS_NAME = "HEADERS"
AUTH_NAME = "AUTH"
ALLOW_REDIRECTS_NAME = "ALLOW REDIRECTS"
JSON_NAME = "JSON"


def find_keywords_begin_and_end(path, section_name):
    """

    :param path: :type path: str
    :param section_name:
    :return: :rtype: list
    """
    begin = path.find("%s" % section_name)

    if begin == -1:
        return -1, -1

    begin = begin + len(section_name) + 1
    end = path.find(",", begin)
    return begin, end


def extract_section_by_name(path, section_name):
    """

    :param path:
    :type path: str
    :param section_name:
    :type section_name: str
    :return:
    :rtype: str
    """

    begin, end = find_keywords_begin_and_end(path, section_name)

    if begin == -1 and end == -1:
        return None

    if end > 0:
        fragmented = path[begin: end]
    else:
        fragmented = path[begin:]

    return fragmented


def get_digest_auth(tokens):
    """
    author Damian Mirecki

    :param tokens: should be two-element list with username and password
    :type tokens: list
    :return: http auth instance
    :rtype: requests.auth.HTTPDigestAut
    """
    return requests.auth.HTTPDigestAuth(tokens[0], tokens[1])


def get_basic_auth(tokens):
    """
    author Damian Mirecki

    :param tokens: should be two-element list with username and password
    :type tokens: list
    :return: http auth instance
    :rtype: requests.auth.HTTPBasicAuth
    """
    return requests.auth.HTTPBasicAuth(tokens[0], tokens[1])


class Connect(Command):
    """Make request"""

    __metaclass__ = CommandRegister

    pretty_name = "MAKING REQUEST"

    def __init__(self, result_collector):
        super(Connect, self).__init__(result_collector)
        self.params = {}
        self.headers = {}
        self.url = ""
        self.arguments = ""

    def parse_params(self, path):
        section = extract_section_by_name(self.arguments, PARAMS_NAME)

        if section is None:
            return

        fragmented = section.split(" ")
        for i in range(0, len(fragmented) / 2):
            self.params[fragmented[2 * i]] = fragmented[2 * i + 1]

    def parse_headers(self, path):
        section = extract_section_by_name(self.arguments, HEADERS_NAME)

        if section is None:
            return

        fragmented = section.split(" ")
        for i in range(0, len(fragmented) / 2):
            self.headers[fragmented[2 * i]] = fragmented[2 * i + 1]

    def parse_url(self, path):
        args = path.split(" ")
        if len(args) < 1 or len(args[0]) < 1:
            raise indor_exceptions.URLNotFound("Nie podano adres URL")
        self.url = args[0].rstrip(",")

    def get_auth(self):
        """
        Method use simple grammar to parse auth params. For the present we support basic and digest auth,
        but I think that we can support e.g. OAuth1, OAuth2 in future.

        author Damian Mirecki

        :return: variable that should be pass as auth when making request, see parse method
        :rtype: requests.auth.HTTPBasicAuth|requests.auth.HTTPDigestAuth|list
        """
        fragmented = extract_section_by_name(self.arguments, AUTH_NAME)

        if fragmented is None:
            return []

        username = Word(printables)
        password = Word(printables)

        basic_auth = (Optional(Suppress("BASIC")) + username + password).setParseAction(get_basic_auth)
        digest_auth = (Suppress("DIGEST") + username + password).setParseAction(get_digest_auth)
        auth = digest_auth | basic_auth

        return auth.parseString(fragmented)[0]

    def parse(self, path):
        argument = path[0]

        arguments = " ".join(path[1:])
        self.arguments = arguments

        self.parse_params(arguments)
        self.parse_headers(arguments)
        try:
            self.parse_url(arguments)
        except indor_exceptions.URLNotFound as e:
            self.result_collector.add_result(Error(self, e))
            return

        try:
            func = getattr(requests, argument.lower())
        except AttributeError:
            self.result_collector.add_result(
                Error(self, indor_exceptions.TypeRequestNotFound('type not found "%s"' % (argument.lower()))))
            return
        else:
            self.result_collector.set_response(func(url=self.url, data=self.params, auth=self.get_auth(),
                                                    allow_redirects=self.get_allow_redirects()))

    def get_allow_redirects(self):
        """
        Check if name ALLOW REDIRECTS is in arguments-string.

        :return:
        :rtype: bool
        """
        return ALLOW_REDIRECTS_NAME in self.arguments



CommandFactory().add_class(Connect.__name__, Connect)