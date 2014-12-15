#-*- coding: utf-8 -*-

from indor_exceptions import InvalidRelationalOperator


def compare_by_relational_operator(actual, relational_operator, expected):
    # TODO - Nie podoba mi się to
    # Nie wydaje mi się, że powinniśmy to w taki sposób robić
    # Eval jest brzydki, niebezpieczny i wolny
    # Używamy również operatorów Pythona
    # Robimy konwersje do stringa
    # Może po prostu użyć ___eq___, ___gt___, ___nt___
    return eval(str(actual) + " " + relational_operator + " " + str(expected))


def extract_relational_operator(supposed_operator):
    """
    Function removes extra spaces, check if given operator is valid
    and replace ambiguous operator, e.g. replace "=" with "=="

    :param supposed_operator:
    :type supposed_operator: str
    :return: :rtype: str :raise InvalidRelationalOperator:
    """
    equality_operators = ["=", "=="]
    inequality_operators = ["!=", "<>"]
    valid_operators = ["<", ">", "<=", ">="]

    supposed_operator = supposed_operator.strip()

    if supposed_operator in equality_operators:
        return "=="

    if supposed_operator in inequality_operators:
        return "!="

    if supposed_operator not in valid_operators:
        raise InvalidRelationalOperator("got '" + supposed_operator + "' but only " + (
            valid_operators + equality_operators + inequality_operators).__str__() + " is accepted")

    return supposed_operator