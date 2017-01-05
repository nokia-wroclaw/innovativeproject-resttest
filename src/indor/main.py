import argparse
import fnmatch
import os

from pyparsing import ParseException

from .general_error import GeneralError, GENERAL_ERROR_PARSE_FAILED, GENERAL_ERROR_FILE_NOT_FOUND
from .printer import Printer
from .reading import read_from_file
from .statistics import Statistics
from . import test_runner
from . import input_parser as parser


def parse_arguments():
    arg_parser = argparse.ArgumentParser(prog="indor", description='Run REST tests')
    arg_parser.add_argument('dir', metavar='FILE|DIR', type=str,
                            help='File or folder with definitions of tests')
    arg_parser.add_argument('--xml', dest='xml_output', action='store_true',
                            help='Print the results in xml format')
    arg_parser.add_argument('--flags', dest='flags', nargs='*', default=[],
                            help='Only scenarios with given flags will be executed')
    arg_parser.add_argument('--filename', dest='filename_pattern', default='*.ind',
                            help='Only files with name matches given pattern will be executed')
    arg_parser.add_argument('--verbose', dest='verbose', action='store_true',
                            help='Print extended information about tests')
    args = arg_parser.parse_args()

    return args


class Indor(object):
    def __init__(self):
        args = parse_arguments()

        self.flags = args.flags
        self.tests_dir = args.dir
        self.filename_pattern = args.filename_pattern

        self.printer = Printer.factory(args.xml_output, args.verbose)
        self.statistics = Statistics()

        self.run_tests()

    def run_test(self, file_path):
        results = self.get_results_from_file(file_path)

        self.statistics.collect_statistics(results)
        self.printer.collect_summary(results, file_path)

    def run_tests_files(self, test_files_paths):
        for file_path in test_files_paths:
            self.run_test(file_path)

    def run_tests(self):
        test_files_paths = self.get_test_files_paths()

        self.printer.print_initial_information()

        self.statistics.tests_started()
        self.printer.tests_started()

        self.run_tests_files(test_files_paths)

        self.printer.tests_finished()
        self.statistics.tests_finished()

        self.printer.print_statistics(self.statistics)

    def get_results_from_file(self, file_path):
        try:
            file_data = read_from_file(file_path)
            test_data = parser.parse(file_data)
            runner = test_runner.TestsRunner(self.flags)
            results = runner.run(test_data)
        except IOError:
            results = [GeneralError("{} {}".format(GENERAL_ERROR_FILE_NOT_FOUND, file_path))]
        except ParseException:
            results = [GeneralError("{} {}".format(GENERAL_ERROR_PARSE_FAILED, file_path))]
        #except Exception as e:
        #    results = [GeneralError("{}({}) {} {}".format(GENERAL_ERROR_UNKNOWN_ERROR, e.__class__.__name__, file_path, e.message))]
        return results

    def get_test_files_paths(self):
        if os.path.isdir(self.tests_dir):
            return [os.path.join(dp, f) for dp, dn, filenames in os.walk(self.tests_dir) for f in filenames if
                    fnmatch.fnmatch(f, self.filename_pattern)]

        return [self.tests_dir]


def main():
    Indor()
Indor()
