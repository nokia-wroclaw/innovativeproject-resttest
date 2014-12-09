# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import re
from pyparsing import *


def remove_comments(test_data):
    """

    :param test_data:
    :type test_data: str
    :return: :rtype: str
    """
    inline_comment = Suppress(Literal("#") + SkipTo(lineEnd))
    multi_line_comment = nestedExpr('/%', '%/').suppress()
    comments = inline_comment | multi_line_comment

    return comments.transformString(test_data)


def parse_token(token):
    if token.startswith("\"") and token.endswith("\""):
        ready_token = token[1:-1]
    else:
        ready_token = token[:]

    if token.endswith("."):
        parse_token.expression += [token[:-1]]
        returned = parse_token.expression[:]
        parse_token.expression = []
        return returned
    else:
        parse_token.expression += [ready_token]
        return None


def parse(input_data):
    ParserElement.setDefaultWhitespaceChars(" \t\n\r")

    hashmark = '#'
    multi_line_comment_start = '/%'
    multi_line_comment_end = '%/'

    inline_comment = hashmark + restOfLine
    multi_line_comment = nestedExpr(multi_line_comment_start, multi_line_comment_end)
    comment = multi_line_comment | inline_comment

    quoted_string = QuotedString("\"", multiline=True, escQuote="\"", unquoteResults=False)
    word = Word(printables)

    token = quoted_string | word
    parser = ZeroOrMore(token)
    parser.ignore(comment)


    all_tokens = parser.parseString(input_data)

    parse_token.expression = []

    unfiltered_expressions = map(lambda token: parse_token(token), all_tokens)

    return filter(lambda expression: expression is not None, unfiltered_expressions)