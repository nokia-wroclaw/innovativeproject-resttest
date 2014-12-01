# coding=utf-8
from connect import Connect
from printer import Printer

__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'
from requests.structures import CaseInsensitiveDict
from asserts import AssertResponseStatus, AssertResponseNotEmpty, AssertResponseTypeJson, AssertResponseLengthGreater, \
    AssertResponseEmpty, AssertResponseRedirectsCount, AssertCookieSet, AssertCookieValue, AssertPathExists, \
    AssertPathNodesCountEqual, AssertPathNodesCountGreater, AssertPathNodesCountLess, AssertPathContainsAny, \
    AssertPathContainsEach, AssertPathFinal
from test import Test
from result_collector import ResultCollector


class TestsRunner:
    assertions_names = CaseInsensitiveDict()

    def __init__(self):
        self.response = None
        self.result_collector = ResultCollector(self)
        TestsRunner.request = None

    def run(self, test_lines):
        for test_data in test_lines:
            test = Test(self.result_collector)
            test.parse(test_data)

        Printer(self.result_collector.scenarios).print_summary()
