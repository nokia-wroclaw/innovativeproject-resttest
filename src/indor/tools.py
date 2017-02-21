from requests.status_codes import _codes
from requests.structures import CaseInsensitiveDict

from . import indor_exceptions
from .indor_exceptions import InvalidStatusCodeName, InvalidStatusCode


def get_parent_module_name(module_name):
    parent_name, _, child_name = module_name.rpartition('.')
    return parent_name


def transform_nested_array(array, transform):
    return [transform_nested_array(x, transform) if isinstance(x, (list, tuple)) else transform(x) for x in array]


def create_key_value_pairs(section):
    """

    :param section:
    :type section: list
    :return:
    :rtype: dict
    """
    return dict(zip(section[0::2], section[1::2]))


def extract_section_by_name(path, section_name):
    """

    :param path:
    :type path: list
    :param section_name:
    :type section_name: str
    :return:
    :rtype: list|None
    """

    sections_params = _extract_section_by_name([path], section_name)

    if sections_params is not None:
        return sections_params

    return _extract_section_by_name(path, section_name)


def _extract_section_by_name(path, section_name):
    section = section_name.split(" ")
    predicate = lambda x, s: s == x[:len(s)]

    return next((x[len(section):] for x in path if predicate(x, section)), None)


def parse_url_with_type(path):
    if isinstance(path[0], list):
        if len(path[0]) != 2:
            raise indor_exceptions.URLNotFound("Nie podano adres URL")
        return path[0][0], path[0][1]

    if len(path) < 2:
        raise indor_exceptions.URLNotFound("Nie podano adres URL")

    return path[0], path[1]


_response_status_mapping = CaseInsensitiveDict()
_response_status_mapping["Ok"] = 200
_response_status_mapping["Not found"] = 404


def _map_status_code(status):
    """

    author Damian Mirecki

    :param status
    :return:
    :rtype: int
    :raise LookupError: When status is not implemented yet.
    """

    if status not in _response_status_mapping:
        raise LookupError("Status " + status + " not found in " + _response_status_mapping.__str__())

    return _response_status_mapping[status]


def parse_response_status(status):
    if not status.isdigit():
        try:
            status = _map_status_code(status)
        except LookupError as e:
            raise InvalidStatusCodeName(str(e)) from e
    else:
        if int(status) not in _codes.keys():
            raise InvalidStatusCode(status)
    return int(status)


def parse_url(path, section_name):
    section_with_url = extract_section_by_name(path, section_name)

    if section_with_url is None or len(section_with_url) > 1:
        raise indor_exceptions.URLNotFound("Nie podano adres URL")
    return section_with_url[0]
