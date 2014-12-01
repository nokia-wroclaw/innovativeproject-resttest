# coding=utf-8
from printer import Printer

__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'
from test import Test
from result_collector import ResultCollector


class TestsRunner:
    def __init__(self):
        self.response = None
        self.result_collector = ResultCollector(self)
        TestsRunner.request = None

    def run(self, test_lines):
        for test_data in test_lines:
            test = Test(self.result_collector)
            test.parse(test_data)

        Printer(self.result_collector.scenarios).print_summary()
