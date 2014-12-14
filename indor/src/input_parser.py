# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import re
from pyparsing import *

word = Regex('[a-zA-Z0-9.><=:/$&+;?@|^*()%!-_]*[a-zA-Z0-9><=:/$&+;?@|^*()%!-]')


def flat_list(x):
    """
    If there is list [["sth, "sth"]] then this method return just ["sth", "sth"].
    If x = ["sth", "sth"] method return ["sth", "sth"]

    :param x:
    :type x: list
    :return:
    :rtype: list
    """
    if len(x) == 1:
        return x[0]
    return x


def parse_constants(input_data):
    # Getting all defined macros
    const_definition = Suppress("DEFINE") + word + Suppress("=") + empty + restOfLine
    constants = dict(list(const_definition.searchString(input_data)))

    # Replacing consts values in input text
    constants_replaced = input_data
    for key, value in constants.items():
        const = Literal("@") + Literal(key) + Literal("@")
        const.setParseAction(replaceWith(value))
        constants_replaced = const.transformString(constants_replaced)

    # Removing consts definitions
    const_definition.setParseAction(replaceWith(""))
    return const_definition.transformString(constants_replaced)


def parse(input_data):
    consts_replaced = parse_constants(input_data)

    hashmark = '#'
    multi_line_comment_start = '/%'
    multi_line_comment_end = '%/'

    inline_comment = hashmark + restOfLine
    multi_line_comment = nestedExpr(multi_line_comment_start, multi_line_comment_end)
    comment = multi_line_comment | inline_comment

    quoted_string = QuotedString("\"", multiline=True, escQuote="\"", unquoteResults=True)
    expression_in_bracket = originalTextFor(nestedExpr("{", "}"))  # I hate it. I really hate it. I spent 1.5 h on it,
    # checked 1000000000 ways of do it and finally
    # I added only half a line. I hate it.

    token = expression_in_bracket | quoted_string | word

    sub_command = Group(OneOrMore(token) + Optional(Literal(",").suppress()))
    command = Group(OneOrMore(sub_command) + ("." + LineEnd()).suppress())

    parser = OneOrMore(command)
    parser.ignore(comment)

    all_commands = parser.parseString(consts_replaced).asList()
    return map(flat_list, all_commands)