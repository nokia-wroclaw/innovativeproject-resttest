from abc import ABCMeta, abstractmethod
import sys

from junit_xml import TestSuite, TestCase
from termcolor import cprint, colored

from general_error import GeneralError
from result import Passed, Failed, Error, ConnectionError


class Printer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def print_summary(self, results):
        pass

    @abstractmethod
    def print_statistics(self, statistics, file_path):
        pass

    def factory(xml_output):
        """
        :rtype : Printer
        """
        if xml_output:
            return JunitXMlPrinter()
        else:
            return ConsolePrinter()

        assert 0, "Bad shape creation: " + type

    factory = staticmethod(factory)


class ConsolePrinter(Printer):
    def print_statistics(self, statistics):
        sys.stdout.write(
            "{} scenarios, {} tests and {} assertions (".format(statistics.scenarios_count, statistics.tests_count,
                                                                statistics.assertions_count))
        sys.stdout.write(colored("{} failed".format(statistics.failed_count), 'red'))
        sys.stdout.write(", ")
        sys.stdout.write(colored("{} passed".format(statistics.passed_count), 'green'))
        sys.stdout.write(")\n")
        print "within", statistics.get_tests_time()

    def print_summary(self, results, file_path):
        for scenario_result in results:
            self.print_scenario_result(scenario_result, file_path)
            print

    def print_scenario_result(self, scenario_result, file_path):
        if isinstance(scenario_result, GeneralError):
            cprint("    ERROR: " + scenario_result.message, 'red')
            return

        sys.stdout.write("Scenario ")
        sys.stdout.write(colored("\"{}\"".format(scenario_result.name), 'cyan'))
        sys.stdout.write(" with flags: ")
        sys.stdout.write(colored(scenario_result.flags, 'cyan'))

        sys.stdout.write("    # {}\n".format(file_path))

        for test_result in scenario_result.test_results:
            self.print_test_result(test_result)

    def print_test_result(self, test_result):
        print("  Test {}".format(test_result.name))
        for assertion_result in test_result.results:
            self.print_assertion_result(assertion_result)

    def print_assertion_result(self, assertion_result):
        if isinstance(assertion_result, Passed):
            cprint("    PASSED: {}".format(assertion_result.pretty_name), 'green')
        elif isinstance(assertion_result, Failed):
            cprint("    FAILED: {}\n      EXPECTED {}\tGOT {}"
                   .format(assertion_result.pretty_name, assertion_result.expected, assertion_result.actual), 'red')
        elif isinstance(assertion_result, (Error, ConnectionError)):
            cprint("    ERROR: {}\n      {}".format(assertion_result.pretty_name, assertion_result.error), 'red')
        else:
            print("\t\t ASSERTION: {}\n\t\tUNKNOWN RESULT".format(assertion_result.pretty_name))


# TODO: Unit tests!!!
class JunitXMlPrinter(Printer):
    def print_statistics(self, statistics):
        pass

    def print_summary(self, results, file_path):
        test_suites = []
        for scenario_result in results:
            if isinstance(scenario_result, GeneralError):
                test_suite = TestSuite("", "")
                test_suites.append(test_suite)
                test_case = TestCase("", "")
                test_case.add_error_info(scenario_result.message)
                test_suite.test_cases.append(test_case)
                continue

            test_suite = TestSuite(scenario_result.name)
            for test_result in scenario_result.test_results:
                test_case = TestCase(test_result.name, test_result.name)
                for result in test_result.results:
                    if isinstance(result, Failed):
                        test_case.add_failure_info("ASSERTION {} failed".format(result.pretty_name),
                                                   "EXPECTED {}\nGOT {}".format(result.expected,
                                                                                result.actual))
                    elif isinstance(result, (Error, ConnectionError)):
                        test_case.add_error_info("ASSERTION {} failed".format(result.pretty_name),
                                                 "ERROR {}".format(result.error))
                    elif isinstance(result, Passed):
                        pass
                    # TODO: What to do below?
                    else:
                        raise Exception("Unknown state")
                test_suite.test_cases.append(test_case)
            test_suites.append(test_suite)
        print(TestSuite.to_xml_string(test_suites))