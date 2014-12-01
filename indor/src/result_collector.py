from scenario_data import ScenarioData


class ResultCollector(object):
    def __init__(self, test_runner):
        self.test_runner = test_runner
        self.scenarios = []

    def set_response(self, response):
        self.test_runner.response = response
        if len(self.scenarios) == 0:
            self.scenarios.append(ScenarioData("ANONYMOUS", []))
        self.scenarios[-1].add_test(response.url)

    def get_response(self):
        return self.test_runner.response

    def add_result(self, result):
        self.scenarios[-1].add_result(result)

    def visit_by_scenario(self, scenario_data):
        self.scenarios.append(ScenarioData(scenario_data.name, scenario_data.flags))
        last_test_name = self.scenarios[-2].get_last_test_name()
        self.scenarios[-1].add_test(last_test_name)