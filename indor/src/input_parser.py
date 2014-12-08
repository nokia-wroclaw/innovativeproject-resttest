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


def parse(input_data):
    # # no_comments
    # no_comment = re.sub(r'#.*', "", input_data)
    # no_big_comment = re.sub(r'/%(.|\n)*%/', "", no_comment)
    #
    # # blank spaces
    # parsed1 = re.sub(r'\s+', " ", no_big_comment).replace(". ", "\n")
    # parsed2 = re.sub(r'^\s+', "", parsed1)
    # parsed3 = re.sub(r'\.$', "", parsed2)
    #
    # # strings in quotes
    # within_quotes = re.findall('"([^"]*)"', parsed3)
    # for within_quote in within_quotes:
    #     escaped = re.sub("\s", "<QUOTES_BLANK>", within_quote)
    #     parsed3 = re.sub(within_quote, escaped, parsed3)
    #
    # # splitting lines
    # test_lines = parsed3.splitlines()
    # parsed4 = map(lambda x: x.split(" "), test_lines)
    # parsed = map(lambda x: map(lambda y: re.sub("<QUOTES_BLANK>", " ", y), x), parsed4)

    ParserElement.setDefaultWhitespaceChars(" \t\n\r")


    no_comments = remove_comments(input_data)

    p = delimitedList(Regex('([a-zA-z0-9/\,: \t\n]|(\.[^\n]))*'), Literal('.') + lineEnd)

    return p.parseString(no_comments)

    # # Exclude newlines from the default whitespace characters.
    # # We need to deal with them manually.
    # ws = ' \t'
    # ParserElement.setDefaultWhitespaceChars(ws)
    #
    #
    # # Define punctuation and legal characters.
    # backslash = '\\'
    # hashmark = '#'
    # standard_chars = printables.replace(backslash, '').replace(hashmark, '')
    #
    # # Escape codes.
    # escaped_hash = Literal(backslash + hashmark)
    # escaped_backslash = Literal(backslash + backslash)
    # escape = (backslash + Word(printables, exact=1)) | escaped_hash | escaped_backslash
    #
    # # Free-form text includes internal whitespace, but not leading or trailing.
    # text = OneOrMore(White(ws) | Word(standard_chars) | escape)
    # text.setParseAction(lambda tokens: ''.join(tokens))
    #
    # comment = (hashmark + restOfLine).suppress()
    #
    # # Define line-related parts.
    # EOL = LineEnd().suppress()
    # SOL = LineStart().leaveWhitespace()
    # continuation = (Literal(backslash).leaveWhitespace() + EOL).suppress()
    # blankline = SOL + LineEnd()
    #
    #
    # # Define parts of the document and the parser.
    # physical_line = text + EOL
    # physical_line.setParseAction(lambda tokens: tokens[0].rstrip())
    # logical_line = OneOrMore(text + continuation) + physical_line
    # logical_line.setParseAction(lambda tokens: ''.join([x.lstrip() for x in tokens]))
    #
    # line = physical_line | logical_line | EOL
    # body = OneOrMore(line)
    # parser = body + StringEnd()
    # parser.ignore(blankline)
    # parser.ignore(comment)
    #
    # data = r"""# this is a comment
    #   # comment with leading whitespace
    # line 1
    # line 2
    #
    # line 3 # has a comment
    # line 4 \# does not have a comment
    # line 5 \
    #   continues over three \
    #   physical lines
    #
    # line 6 \
    #
    #   continues over two physical lines, with a blank in between
    #
    # line 7 doesn't continue \\
    # line \8 in\cludes \escapes (and also a\ bug).
    #     line 9 also has a comment # which gets rid of this backslash \
    # and lastly line 10.
    #
    # """
    # # test_line = OneOrMore(Word(printables) | White())
    # # #test_line = nestedExpr(lineStart, '.' + lineEnd)
    # # return delimitedList(test_line, '.' + lineEnd).parseString(no_comments)
