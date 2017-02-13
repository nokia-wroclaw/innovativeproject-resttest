from . import indor_exceptions


def get_parent_module_name(module_name):
    parent_name, _, child_name = module_name.rpartition('.')
    return parent_name


def transform_nested_array(array, transform):
    return [transform_nested_array(x, transform) if isinstance(x, (list, tuple)) else transform(x) for x in array]


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


def parse_url_with_type(path):
    if isinstance(path[0], list):
        if len(path[0]) < 2:
            raise indor_exceptions.URLNotFound("Nie podano adres URL")
        return path[0][0], path[0][1]

    if len(path) < 2:
        raise indor_exceptions.URLNotFound("Nie podano adres URL")

    return path[0], path[1]


def parse_url(path):
    if isinstance(path[0], list):
        if len(path[0]) < 1:
            raise indor_exceptions.URLNotFound("Nie podano adres URL")
        return path[0][0]

    if len(path) < 1:
        raise indor_exceptions.URLNotFound("Nie podano adres URL")

    return path[0]