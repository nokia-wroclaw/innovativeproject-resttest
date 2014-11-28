# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import sys
import os

import test_runner
import input_parser as parser


def read_from_file(filename):
    this_dir, this_filename = os.path.split(__file__)

    logo_file_path = os.path.join(this_dir, "logo.txt")
    logo_file = open(logo_file_path, "r")
    logo = logo_file.read()
    print(logo)

    f = open(filename, "r")

    file_data = f.read()
    test_data = parser.parse(file_data)

    runner = test_runner.TestRunner()
    runner.run(test_data)

    f.close()


args = sys.argv

if len(args) != 2:
    print("Usage: python main.py file.ind")
    sys.exit()

read_from_file(args[1])