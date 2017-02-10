import re
from .test_results import TestResults
from .scenario_data import ScenarioData
from .scenario_results import ScenarioResults
from .xml_tree_factory import XmlTreeFactory


class ResultCollector(object):
    def __init__(self, test_runner, flags):
        self.test_runner = test_runner
        self.flags = set(flags)
        self.scenarios = []
        self.execute_current_scenario = True
        self.variables = {}

    def add_variable(self, name, value):
        self.variables[name] = value

    def use_variables(self, string):
        variables = re.findall(r'\$[a-zA-Z0-9]+\$', string)
        for var in variables:
            string = string.replace(var, self.variables[var])
        return string

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
        scenario_results = ScenarioResults(scenario_data)
        if self.is_scenario_executed(scenario_results):
            self.scenarios.append(scenario_results)
            self.execute_current_scenario = True
        else:
            self.execute_current_scenario = False
        # TODO: Why would we need the next line? It doesn't seem to be working
#        self.scenarios[-1].add_test(self.scenarios[-2].get_last_test())

    def get_response_ElementTree(self):
        if self.test_runner.responseXML is None:
            if self.test_runner.parser is None:
                contentType = self.test_runner.response.headers.get('content-type')
                t = contentType[:contentType.index(';')]
                t = t.split("/")
                class_name = ""
                for i in range(0,len(t)):
                    class_name += t[i].lower().title()
            else:
                class_name = self.test_runner.parser
            tree = XmlTreeFactory().get_class(class_name)
            self.test_runner.responseXML = tree.parse(self.test_runner.response.content)
        return self.test_runner.responseXML

    def set_parser(self, name):
        if name.lower() == "default":
            self.test_runner.parser = None
            self.test_runner.responseXML = None
        else:
            self.test_runner.parser = name
            self.test_runner.responseXML = None

    def is_scenario_executed(self, scenario):
        if not self.flags:
            return True
        return len(self.flags.intersection(scenario.flags)) > 0