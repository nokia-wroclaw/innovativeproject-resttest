# coding=utf-8
from general_error import GeneralError

__author__ = 'Sławomir Domagała'
from result import Passed, Failed, Error, ConnectionError


class Printer:
    def __init__(self, scenarios_results):
        self.scenarios_results = scenarios_results

    def print_summary(self):
        print("Execution finished")
        for scenario_result in self.scenarios_results:
            if isinstance(scenario_result, GeneralError):
                print("ERROR: " + scenario_result.message)
                continue

            print("Scenario \"{}\" with flags: {}".format(scenario_result.name, scenario_result.flags))
            for test_result in scenario_result.test_results:
                print("\tTest {}".format(test_result.name))
                for result in test_result.results:
                    if isinstance(result, Passed):
                        print("\t\t ASSERTION: {}\n\t\tPASSED".format(result.pretty_name))
                    elif isinstance(result, Failed):
                        print("\t\t ASSERTION: {}\n\t\tFAILED: EXPECTED {}\tGOT {}"
                              .format(result.pretty_name, result.expected, result.actual))
                    elif isinstance(result, (Error, ConnectionError)):
                        print("\t\t {}\n\t\tERROR: {}".format(result.pretty_name, result.error))
                    else:
                        print("\t\t ASSERTION: {}\n\t\tUNKNOWN RESULT".format(result.pretty_name))