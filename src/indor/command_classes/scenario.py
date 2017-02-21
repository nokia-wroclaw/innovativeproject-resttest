from ..command import Command


class ScenarioData(object):
    def __init__(self, name, flags, repetition_name=None):
        self.name = name
        self.flags = flags
        self.repetition_name = repetition_name


class Scenario(Command):
    def parse(self, path, repetition_name=None):
        self.result_collector.visit_by_scenario(ScenarioData(path[0], path[2:], repetition_name))
