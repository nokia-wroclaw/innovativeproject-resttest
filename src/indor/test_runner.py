__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'
from .test import Test
from .result_collector import ResultCollector


class TestsRunner:
    def __init__(self, flags=[]):
        self.response = None
        self.flags = flags
        self.result_collector = ResultCollector(self, flags)
        self.responseXML = None
        self.parser = None
        TestsRunner.request = None

    def run(self, test_lines):
        for test_data in test_lines:
            test = Test(self.result_collector)
            test.parse(test_data)

        return self.result_collector.scenarios
