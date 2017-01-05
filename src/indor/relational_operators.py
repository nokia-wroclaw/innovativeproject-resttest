import operator
from .indor_exceptions import InvalidRelationalOperator


def compare_by_supposed_relational_operator(actual, supposed_relational_operator, expected):
    """
    Function removes extra spaces, check if given operator is valid
    and replace ambiguous operator, e.g. replace "=" with "=="

    :param supposed_relational_operator:
    :type supposed_relational_operator: str
    :return: :rtype: str :raise InvalidRelationalOperator:
    """
    supposed_relational_operator = supposed_relational_operator.strip()

    operators_mapping = {
        "=": operator.eq,
        "==": operator.eq,
        "!=": operator.ne,
        "<>": operator.ne,
        "<=": operator.le,
        ">=": operator.ge,
        "<": operator.lt,
        ">": operator.gt
    }

    if supposed_relational_operator not in operators_mapping:
        raise InvalidRelationalOperator("Got '" + supposed_relational_operator + "' but only " +
                                        operators_mapping.keys().__str__() + " are valid.")

    compare = operators_mapping[supposed_relational_operator]

    return compare(actual, expected)