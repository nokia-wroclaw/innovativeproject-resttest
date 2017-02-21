import json

from ..result import Error
from ..parsing_exception import ParsingException
from ..indor_exceptions import InvalidStatusCodeName, InvalidStatusCode
from ..command import Command
from ..command_register import CommandRegister
from ..tools import extract_section_by_name, parse_url, parse_response_status, create_key_value_pairs

DATA_NAME = "DATA"
WAITTIME_NAME = "WAITTIME"
STATUS_NAME = "STATUS"

DEFAULT_WAITTIME = 10.0  # seconds
DEFAULT_STATUS = "200"  # OK


def get_data(path):
    section = extract_section_by_name(path, DATA_NAME)

    if section is None:
        return None

    return create_key_value_pairs(section)


def get_waittime(path):
    section = extract_section_by_name(path, WAITTIME_NAME)

    if section is None:
        return DEFAULT_WAITTIME

    return float(section[0]) / 1000.0


def get_status(path):
    section = extract_section_by_name(path, STATUS_NAME)

    if section is None:
        return DEFAULT_STATUS

    return section[0]


class CallbackResponse(object):
    def __init__(self, url, status, waittime, data):
        self.url = url
        self.status = parse_response_status(status)
        self.waittime = waittime
        self.data = data

    def __repr__(self):
        representation = {'url': self.url, 'status': self.status, 'waittime': self.waittime, 'data': self.data}
        return json.dumps(representation)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return repr(other) == repr(self)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented


class HandleRequest(Command, metaclass=CommandRegister):
    pretty_name = "HANDLING REQUEST"

    def __init__(self, result_collector):
        super(HandleRequest, self).__init__(result_collector)

    def parse(self, path):
        try:
            self.result_collector.add_request(
                CallbackResponse(url=parse_url(path, "HANDLE REQUEST"), status=get_status(path),
                                 waittime=get_waittime(path), data=get_data(path)))
        except InvalidStatusCodeName as e:
            raise ParsingException(self, Error.from_exception(self, e))
        except InvalidStatusCode as e:
            raise ParsingException(self, Error.from_exception(self, e))
