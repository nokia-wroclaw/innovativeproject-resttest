import datetime

from .general_error import GeneralError
from .result import Passed, Failed, Error, ConnectionError


class Statistics(object):
    def __init__(self):
        self.scenarios_count = 0
        self.errors_count = 0
        self.tests_count = 0
        self.assertions_count = 0
        self.passed_count = 0
        self.errors_count = 0
        self.failed_count = 0
        self.start_time = None
        self.end_time = None

    def tests_started(self):
        self.start_time = datetime.datetime.now()

    def tests_finished(self):
        if self.start_time is None:
            raise Exception("Start time must be set")

        self.end_time = datetime.datetime.now()

    def get_tests_time(self):
        if self.start_time is None or self.end_time is None:
            raise Exception("Start and end time must be set")

        return self.end_time - self.start_time

    def collect_statistics(self, scenario_results):
        for scenario_result in scenario_results:
            self.scenarios_count += 1

            if isinstance(scenario_result, GeneralError):
                self.errors_count += 1
                continue

            for test_result in scenario_result.test_results:
                self.tests_count += 1
                for result in test_result.results:
                    self.assertions_count += 1
                    if isinstance(result, Passed):
                        self.passed_count += 1
                    elif isinstance(result, Failed):
                        self.failed_count += 1
                    elif isinstance(result, (Error, ConnectionError)):
                        self.errors_count += 1
