import sys
from reading import read_from_file
import test_runner
import input_parser as parser
from printer import Printer

__author__ = 'slawomir'

args = sys.argv

if len(args) != 2:
    print("Usage: python main.py file.ind")
    sys.exit()

file_data = read_from_file(args[1])

test_data = parser.parse(file_data)
runner = test_runner.TestsRunner()
result = runner.run(test_data)

Printer(result).print_summary()
