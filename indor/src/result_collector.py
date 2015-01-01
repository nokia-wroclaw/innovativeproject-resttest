from test_results import TestResults
from scenario_data import ScenarioData
from scenario_results import ScenarioResults
from xml_tree_factory import XmlTreeFactory


class ResultCollector(object):
    def __init__(self, test_runner):
        self.test_runner = test_runner
        self.scenarios = []

    def add_default_scenario(self):
        self.scenarios.append(ScenarioResults(ScenarioData("ANONYMOUS", [])))

    def set_response(self, response):
        self.test_runner.response = response

    def add_test(self, test_name):
        if len(self.scenarios) == 0:
            self.add_default_scenario()
        self.scenarios[-1].add_test(TestResults(test_name))

    def get_response(self):
        return self.test_runner.response

    def add_result(self, result):
        if len(self.scenarios) == 0:
            self.scenarios.append(ScenarioResults(ScenarioData("ANONYMOUS", [])))
        self.scenarios[-1].add_result(result)

    def visit_by_scenario(self, scenario_data):
        self.scenarios.append(ScenarioResults(scenario_data))
        self.scenarios[-1].add_test(self.scenarios[-2].get_last_test())

    def get_response_ET(self):
        if self.test_runner.responseXML == None:
            tree = XmlTreeFactory().get_class(self.test_runner.response.headers.get('content-type'))
            self.test_runner.responseXML = tree.parse(self.test_runner.response.content)
        return self.test_runner.responseXML