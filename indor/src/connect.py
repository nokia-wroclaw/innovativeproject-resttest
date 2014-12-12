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


def extract_section_by_name(path, section_name):
    """

    :param path:
    :type path: list
    :param section_name:
    :type section_name: str
    :return:
    :rtype: list|None
    """

    section = section_name.split(" ")

    predicate = lambda x, section: section == x[:len(section)]

    try:
        return next(x[len(section):] for x in path if predicate(x, section))
    except StopIteration:
        return None


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


def get_allow_redirects(path):
    """
    Check if name ALLOW REDIRECTS is in arguments-string.

    :return:
    :rtype: bool
    """
    return extract_section_by_name(path, ALLOW_REDIRECTS_NAME) is not None


def get_auth(path):
    """
    Method use simple grammar to parse auth params. For the present we support basic and digest auth,
    but I think that we can support e.g. OAuth1, OAuth2 in future.

    author Damian Mirecki

    :return: variable that should be pass as auth when making request, see parse method
    :rtype: requests.auth.HTTPBasicAuth|requests.auth.HTTPDigestAuth|None
    """
    fragmented = extract_section_by_name(path, AUTH_NAME)

    if fragmented is None:
        return None

    s = ' '.join(fragmented)

    username = Word(printables)
    password = Word(printables)

    basic_auth = (Optional(Suppress("BASIC")) + username + password).setParseAction(get_basic_auth)
    digest_auth = (Suppress("DIGEST") + username + password).setParseAction(get_digest_auth)
    auth = digest_auth | basic_auth

    return auth.parseString(s)[0]


def get_json(path):
    json = extract_section_by_name(path, JSON_NAME)

    if json is None:
        return None

    return ast.literal_eval(json[0])


def parse_url(path):
    if isinstance(path[0], list):
        return path[0][0], path[0][1]

    return path[0], path[1]


def get_headers(path):
    section = extract_section_by_name(path, HEADERS_NAME)

    if section is None:
        return None

    return dict(zip(section[0::2], section[1::2]))


def get_params(path):
    section = extract_section_by_name(path, PARAMS_NAME)

    if section is None:
        return None

    return dict(zip(section[0::2], section[1::2]))


class Connect(Command):
    """Make request"""

    __metaclass__ = CommandRegister

    pretty_name = "MAKING REQUEST"

    def __init__(self, result_collector):
        super(Connect, self).__init__(result_collector)

    def parse(self, path):
        try:
            request_type, url = parse_url(path)
            func = getattr(requests, request_type.lower())
        except indor_exceptions.URLNotFound as e:
            self.result_collector.add_result(Error(self, e))
            return
        except AttributeError:
            self.result_collector.add_result(
                Error(self, indor_exceptions.TypeRequestNotFound('type not found "%s"' % (request_type.lower()))))
            return
        else:
            self.result_collector.set_response(func(url=url, data=get_params(path), auth=get_auth(path),
                                                    allow_redirects=get_allow_redirects(path),
                                                    json=get_json(path),
                                                    headers=get_headers(path)))
CommandFactory().add_class(Connect.__name__, Connect)