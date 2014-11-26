# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import re


def parse(input_data):
    # comments
    no_comment = re.sub(r'#.*', "", input_data)
    no_big_comment = re.sub(r'/%(.|\n)*%/', "", no_comment)

    # blank spaces
    parsed1 = re.sub(r'\s+', " ", no_big_comment).replace(". ", "\n")
    parsed2 = re.sub(r'^\s+', "", parsed1)
    parsed3 = re.sub(r'\.$', "", parsed2)

    # strings in quotes
    within_quotes = re.findall('"([^"]*)"', parsed3)
    for within_quote in within_quotes:
        escaped = re.sub("\s", "<QUOTES_BLANK>", within_quote)
        parsed3 = re.sub(within_quote, escaped, parsed3)

    # splitting lines
    test_lines = parsed3.splitlines()
    parsed4 = map(lambda x: x.split(" "), test_lines)
    parsed = map(lambda x: map(lambda y: re.sub("<QUOTES_BLANK>", " ", y), x), parsed4)

    return parsed
