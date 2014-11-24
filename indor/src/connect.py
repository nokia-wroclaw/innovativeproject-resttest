from command import Command
from command_factory import CommandFactory
from result import Error
from result_collector import ResultCollector
import indor_exceptions
import requests
from pyparsing import *

PARAMS_NAME = "PARAMS"
HEADERS_NAME = "HEADERS"
AUTH_NAME = "AUTH"


def find_keywords_begin_and_end(path, section_name):
    """

    :param path: :type path: str
    :param section_name:
    :return: :rtype: list
    :raise KeywordNotFound:
    """
    begin = path.find("%s" % section_name)

    if begin == -1:
        raise indor_exceptions.KeywordNotFound(section_name)

    begin = begin + len(section_name) + 1
    end = path.find(",", begin)
    return begin, end

#Maybe better name, eg. extract_section_by_name
def get_part_of_string_by_name_with_split(path, section_name):
    """

    author Damian Mirecki

    :param path:
    :type path: str
    :param section_name: see top of the file (PARAMS_NAME etc.)
    :type section_name: str
    :return: list split by space
    :rtype: list
    """
    return get_part_of_string_by_name(path, section_name).split(" ")

#Maybe better name, eg. extract_section_by_name
#Is it necessary to have function which returns section content with spaces?
#Splliting spaces takes only 10 characters 'split(" ")'
def get_part_of_string_by_name(path, section_name):
    """

    :param path:
    :type path: str
    :param section_name:
    :type section_name: str
    :return:
    :rtype: str
    """

    begin, end = find_keywords_begin_and_end(path, section_name)

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

    def __init__(self):
        self.params = {}
        self.headers = {}
        self.url = ""
        self.arguments = ""

    def parse_params(self, path):
        try:
            fragmented = get_part_of_string_by_name_with_split(self.arguments, PARAMS_NAME)
        #Why do we treat an exception as a normal behaviour?
        except indor_exceptions.KeywordNotFound:
            self.params = {}
        else:
            for i in range(0, len(fragmented) / 2):
                self.params[fragmented[2 * i]] = fragmented[2 * i + 1]

    def parse_headers(self, path):
        try:
            fragmented = get_part_of_string_by_name_with_split(self.arguments, HEADERS_NAME)
        #Why do we treat an exception as a normal behaviour?
        except indor_exceptions.KeywordNotFound:
            self.params = {}
        else:
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
        try:
            fragmented = get_part_of_string_by_name(self.arguments, AUTH_NAME)
        #Why do we treat an exception as a normal behaviour?
        except indor_exceptions.KeywordNotFound:
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
            ResultCollector().add_result(Error(self, e))
            return

        try:
            func = getattr(requests, argument.lower())
        except AttributeError:
            ResultCollector().add_result(Error(self, indor_exceptions.TypeRequestNotFound('type not found "%s"' % (argument.lower()))))
            return
        else:
            ResultCollector().set_response(func(url=self.url, params=self.params, auth=self.get_auth()))

CommandFactory().add_class(Connect.__name__, Connect)