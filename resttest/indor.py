# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import sys
import rest_test
import indor_input_parser as parser

args = sys.argv

if (len(args) != 2):
    print "Usage: python indor.py file.ind"
    sys.exit()

filename = args[1]
f = open(filename, "r")

file_data = f.read()
test_data = parser.parse(file_data)

runner = rest_test.TestRunner()
runner.run_test(test_data)


