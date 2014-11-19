# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import sys
import rest_test
import indor_input_parser as parser
import os

args = sys.argv

if (len(args) != 2):
    print "Usage: python indor.py file.ind"
    sys.exit()

logo_file_path = os.path.join("..", "other", "logo.txt")
logo_file = open(logo_file_path, "r")
logo = logo_file.read()
print(logo)

filename = args[1]
f = open(filename, "r")

file_data = f.read()
test_data = parser.parse(file_data)

runner = rest_test.TestRunner()
runner.run_test(test_data)


