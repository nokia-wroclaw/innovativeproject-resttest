# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'


import re


def parse(input_data):
    # TODO: Unit tests!
    # First tests, then code!
    no_comment = re.sub(r'#.*', "", input_data)
    parsed1 = re.sub(r'\s+', " ", no_comment).replace(". ", "\n")
    parsed2 = re.sub(r'^\s+', "", parsed1)
    parsed3 = re.sub(r'\.$', "", parsed2)

    test_lines = parsed3.splitlines()
    parsed = map(lambda x: x.split(" "), test_lines)

    return parsed
