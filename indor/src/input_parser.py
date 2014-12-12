# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

from pyparsing import *


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


def parse(input_data):
    hashmark = '#'
    multi_line_comment_start = '/%'
    multi_line_comment_end = '%/'

    inline_comment = hashmark + restOfLine
    multi_line_comment = nestedExpr(multi_line_comment_start, multi_line_comment_end)
    comment = multi_line_comment | inline_comment

    quoted_string = QuotedString("\"", multiline=True, escQuote="\"", unquoteResults=True)
    expression_in_bracket = originalTextFor(nestedExpr("{","}"))    # I hate it. I really hate it. I spent 1.5 h on it,
                                                                    # checked 1000000000 ways of do it and finally
                                                                    # I added only half a line. I hate it.
    word = Regex('[a-zA-Z0-9.><=:/$&+;?@|^*()%!-]*[a-zA-Z0-9><=:/$&+;?@|^*()%!-]')

    token = expression_in_bracket | quoted_string | word

    sub_command = Group(OneOrMore(token) + Optional(Literal(",").suppress()))
    command = Group(OneOrMore(sub_command) + ("." + LineEnd()).suppress())

    parser = OneOrMore(command)
    parser.ignore(comment)

    all_commands = parser.parseString(input_data).asList()
    return map(flat_list, all_commands)