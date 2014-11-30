# coding=utf-8
from command import Command
from scenario_data import ScenarioData

__author__ = 'Tomasz M. Wlisłocki'


class Scenario(Command):
    def __init__(self, result_collector):
        super(Scenario, self).__init__(result_collector)

    def parse(self, path):
        self.result_collector.visit_by_scenario(ScenarioData(path[0], path[2:]))
