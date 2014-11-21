# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import sys
import os

import test_runner
import input_parser as parser


args = sys.argv

if len(args) != 2:
    print("Usage: python main.py file.ind")
    sys.exit()

logo_file_path = os.path.join("..", "other", "logo.txt")
logo_file = open(logo_file_path, "r")
logo = logo_file.read()
print(logo)

filename = args[1]
f = open(filename, "r")

file_data = f.read()
test_data = parser.parse(file_data)

runner = test_runner.TestRunner()
runner.run(test_data)


