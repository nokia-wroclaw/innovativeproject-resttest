import json

from ..command import Command
from ..command_register import CommandRegister
from ..tools import extract_section_by_name, parse_url

DATA_NAME = "DATA"
WAITTIME_NAME = "TIMEOUT"
STATUS_NAME = "STATUS"

DEFAULT_WAITTIME = 10   # seconds
DEFAULT_STATUS = 200    # OK


def get_data(path):
    section = extract_section_by_name(path, DATA_NAME)

    if section is None:
        return None

    return dict(zip(section[0::2], section[1::2]))


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
        self.status = status
        self.waittime = waittime
        self.data = data

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            if self.url != other.url:
                return False
            if self.status != other.status:
                return False
            if self.waittime != other.waittime:
                return False
            return json.dumps(self.data) == json.dumps(other.data)
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented


class HandleRequest(Command, metaclass=CommandRegister):
    pretty_name = "HANDLING REQUEST"

    def __init__(self, result_collector):
        super(HandleRequest, self).__init__(result_collector)

    def parse(self, path):
        url = parse_url(path)

        self.result_collector.add_test(url)
        self.result_collector.add_request(CallbackResponse(url=url, status=get_status(path),
                                                           waittime=get_waittime(path), data=get_data(path)))