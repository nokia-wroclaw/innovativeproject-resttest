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


def parse_macros(input_data):
    macro_definition = Suppress("DEFINE") + word + Suppress("=") + empty + restOfLine
    macros = dict(list(macro_definition.searchString(input_data)))

    def substitute_macro(s, l, t):
        match = re.search(r"@(?P<key>\w+)@", t[0])

        if match is not None and match.group("key") in macros:
            return macros[t[0][1:-1]]

    word.setParseAction(substitute_macro)
    replaced_macros = word.transformString(input_data)

    macro_definition.setParseAction(replaceWith(""))
    return macro_definition.transformString(replaced_macros)


def parse(input_data):
    pre_processed = parse_macros(input_data)

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

    all_commands = parser.parseString(pre_processed).asList()
    return map(flat_list, all_commands)