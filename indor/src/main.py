import argparse
from pyparsing import ParseException
from general_error import GeneralError, GENERAL_ERROR_PARSE_FAILED

from junit_xml_printer import JunitXMlPrinter
from reading import read_from_file
import test_runner
import input_parser as parser
from printer import Printer


def main():
    arg_parser = argparse.ArgumentParser(description='Run REST tests')
    arg_parser.add_argument('file', type=str, nargs='?', help='File with definitions of tests')
    arg_parser.add_argument('--xml', dest='xml_output', action='store_true',
                            help='Print the results in xml format')

    args = arg_parser.parse_args()

    try:
        file_data = read_from_file(args.file)
        test_data = parser.parse(file_data)
        runner = test_runner.TestsRunner()
        result = runner.run(test_data)
    except ParseException:
        result = [GeneralError(GENERAL_ERROR_PARSE_FAILED + args.file)]

    if args.xml_output:
        JunitXMlPrinter(result).print_summary()
    else:
        Printer(result).print_summary()


def __main__():
    main()