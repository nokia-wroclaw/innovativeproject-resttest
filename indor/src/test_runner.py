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

        #TW: IMO to narusza DRY jak cholera
        #TW: Czemu robimy to tu a nie w poszczególnych klasach? To najbrzydszy kod jaki widziałem :P
        #SD: W jaki sposób to narusza DRY?
        #SD: Czego klasa odpowiedzialna za testowanie ma wiedzieć, jak się użytkownikowi drukować?
        TestsRunner.assertions_names[AssertResponseTypeJson.__name__] = "RESPONSE CONTENT TYPE IS JSON"
        TestsRunner.assertions_names[AssertResponseLengthGreater.__name__] = "RESPONSE LENGTH GREATER"
        TestsRunner.assertions_names[AssertResponseNotEmpty.__name__] = "RESPONSE NOT EMPTY"
        TestsRunner.assertions_names[AssertResponseEmpty.__name__] = "RESPONSE EMPTY"
        TestsRunner.assertions_names[AssertResponseStatus.__name__] = "RESPONSE STATUS"
        TestsRunner.assertions_names[AssertResponseRedirectsCount.__name__] = "RESPONSE REDIRECTS COUNT"
        TestsRunner.assertions_names[AssertCookieSet.__name__] = "COOKIE SET"
        TestsRunner.assertions_names[AssertCookieValue.__name__] = "COOKIE VALUE"
        TestsRunner.assertions_names[Connect.__name__] = "MAKING REQUEST"
        TestsRunner.assertions_names[AssertPathExists.__name__] = "ASSERT PATH EXISTS"
        TestsRunner.assertions_names[AssertPathContainsAny.__name__] = "ASSERT PATH CONTAINS ANY"
        TestsRunner.assertions_names[AssertPathContainsEach.__name__] = "ASSERT PATH CONTAINS EACH"
        TestsRunner.assertions_names[AssertPathNodesCountEqual.__name__] = "ASSERT PATH NODES COUNT EQUAL"
        TestsRunner.assertions_names[AssertPathNodesCountGreater.__name__] = "ASSERT PATH NODES COUNT GREATER"
        TestsRunner.assertions_names[AssertPathNodesCountLess.__name__] = "ASSERT PATH NODES COUNT LESS"
        TestsRunner.assertions_names[AssertPathFinal.__name__] = "ASSERT PATH FINAL"
        TestsRunner.request = None

    def run(self, test_lines):
        for test_data in test_lines:
            test = Test(self.result_collector)
            test.parse(test_data)

        Printer(self.result_collector.scenarios).print_summary()
