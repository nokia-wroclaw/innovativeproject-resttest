# coding=utf-8
__author__ = 'Tomasz M. Wlisłocki'

# TODO review, I'm not sure it's the very best way to do this
# TODO Summary of every scenario
class Scenario(object):

    def __init__(self, test_runner, scenario_data):
        self.test_runner = test_runner
        self.name = scenario_data[0]
        self.flags = scenario_data[2:]
        self.test_runner.add_scenario(self)

    def set_response(self, response):
        self.test_runner.response = response

    def get_response(self):
        return self.test_runner.response

    def add_result(self, result):
        self.test_runner.tested_classes.append(result)