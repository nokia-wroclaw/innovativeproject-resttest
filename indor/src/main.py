import argparse
import os

from pyparsing import ParseException

from general_error import GeneralError, GENERAL_ERROR_PARSE_FAILED
from printer import Printer
from reading import read_from_file
from statistics import Statistics
import test_runner
import input_parser as parser


def print_logo():
    this_dir, this_filename = os.path.split(__file__)
    logo_file_path = os.path.join(this_dir, "logo.txt")
    logo_file = open(logo_file_path, "r")
    logo = logo_file.read()
    print(logo)


def get_results_from_file(flags, file_path):
    try:
        file_data = read_from_file(file_path)
        test_data = parser.parse(file_data)
        runner = test_runner.TestsRunner(flags)
        results = runner.run(test_data)
    except ParseException:
        results = [GeneralError(GENERAL_ERROR_PARSE_FAILED + file_path)]
    return results


def main():
    arg_parser = argparse.ArgumentParser(prog="indor", description='Run REST tests')
    arg_parser.add_argument('dir', metavar='FILE|DIR', type=str,
                            help='File or folder with definitions of tests')
    arg_parser.add_argument('--xml', dest='xml_output', action='store_true',
                            help='Print the results in xml format')
    arg_parser.add_argument('--flags', dest='flags', nargs='*', default=[],
                            help='Only scenarios with given flags will be executed')

    args = arg_parser.parse_args()

    print_logo()

    printer = Printer.factory(args.xml_output)
    statistics = Statistics()

    if os.path.isdir(args.dir):
        file_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(args.dir) for f in filenames]
    else:
        file_paths = [args.dir]

    statistics.set_tests_start()

    for file_path in file_paths:
        try:
            results = get_results_from_file(args.flags, file_path)
        except Exception as e:
            results = [GeneralError(str(e.message))]
        finally:
            statistics.collect_statistics(results)
            printer.print_summary(results, file_path)

    statistics.set_tests_finished()

    printer.print_statistics(statistics)


def __main__():
    main()