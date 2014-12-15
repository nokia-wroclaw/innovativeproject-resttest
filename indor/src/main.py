import sys
from junit_xml_printer import JunitXMlPrinter
from reading import read_from_file
import test_runner
import input_parser as parser
from printer import Printer
import argparse
args = sys.argv

arg_parser = argparse.ArgumentParser(description='Run REST tests')
arg_parser.add_argument('file', type=str, nargs='?', help='File with definitions of tests')
arg_parser.add_argument('--xml', dest='xml_output', action='store_true',
                        help='Print the results in xml format')

args = arg_parser.parse_args()

file_data = read_from_file(args.file)

test_data = parser.parse(file_data)
runner = test_runner.TestsRunner()
result = runner.run(test_data)

if args.xml_output:
    JunitXMlPrinter(result).print_summary()
else:
    Printer(result).print_summary()
