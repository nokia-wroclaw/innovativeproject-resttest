from .command import Command
from .scenario_data import ScenarioData


class Scenario(Command):
    def parse(self, path, repetition_name=None):
        self.result_collector.visit_by_scenario(ScenarioData(path[0], path[2:], repetition_name))
