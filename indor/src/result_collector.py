class ResultCollector(object):
    def __init__(self, test_runner):
        self.test_runner = test_runner

    def set_response(self, response):
        self.test_runner.response = response

    def get_response(self):
        return self.test_runner.response

    def add_result(self, result):
        self.test_runner.tested_classes.append(result)

    def visit_by_scenario(self, scenario_data):
        pass