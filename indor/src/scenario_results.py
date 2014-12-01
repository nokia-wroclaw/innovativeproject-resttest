__author__ = 'Sławomir Domagała'
from test_results import TestResults


class ScenarioResults:
    def __init__(self, scenario_data):
        self.name = scenario_data.name
        self.flags = scenario_data.flags
        self.test_results = []

    def add_test(self, url):
        self.test_results.append(TestResults(url))

    def add_result(self, result):
        self.test_results[-1].add_result(result)

    def get_last_test_name(self):
        if len(self.test_results) == 0:
            return None
        else:
            return self.test_results[-1].name