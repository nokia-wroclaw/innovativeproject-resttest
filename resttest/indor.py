# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import sys
import rest_test

args = sys.argv

if (len(args) != 2):
    print "Usage: python indor.py file.ind"
    sys.exit()

filename = args[1]
f = open(filename, "r")

test_data = f.read()
test_lines = test_data.splitlines()

runner = rest_test.TestRunner()
runner.run_test(test_lines)


