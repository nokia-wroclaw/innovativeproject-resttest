# coding=utf-8
from connect import Connect
from result import Passed, Failed, Error

__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'
from requests.structures import CaseInsensitiveDict
from asserts import AssertResponseStatus, AssertResponseNotEmpty, AssertResponseTypeJson, AssertResponseLengthGreater, \
    AssertResponseEmpty, AssertResponseRedirectsCount
from test import Test
from result_collector import ResultCollector

# Sławek
# TODO
# * Dlaczego tyle niepotrzebnych dziedziczeń?
# * Zrobić osobną klasę na TestRunner.assertion_names?
# * Gdzie przechwytujemy wyjątki (bo gdzie rzucamy wiadomo), np. użytkownik podał za małą liczbę argumentów albo za małą ich liczbę


class TestRunner:
    assertions_names = CaseInsensitiveDict()

    def __init__(self):
        self.response = None
        self.tested_classes = []  # list of all classes created in this test
        ResultCollector(self)

        # TODO IMO to narusza DRY jak cholera
        TestRunner.tested_classes = []
        TestRunner.assertions_names[AssertResponseTypeJson.__name__] = "RESPONSE CONTENT TYPE IS JSON"
        TestRunner.assertions_names[AssertResponseLengthGreater.__name__] = "RESPONSE LENGTH GREATER"
        TestRunner.assertions_names[AssertResponseNotEmpty.__name__] = "RESPONSE NOT EMPTY"
        TestRunner.assertions_names[AssertResponseEmpty.__name__] = "RESPONSE EMPTY"
        TestRunner.assertions_names[AssertResponseStatus.__name__] = "RESPONSE STATUS"
        TestRunner.assertions_names[AssertResponseRedirectsCount.__name__] = "RESPONSE REDIRECTS COUNT"
        TestRunner.assertions_names[Connect.__name__] = "MAKING REQUEST"
        TestRunner.request = None

    def print_summary(self):
        print("Tests finished")
        print("Executed tests:")
        for result in self.tested_classes:
            if isinstance(result, Passed):
                print("\t ASSERTION: {}\n\t\tPASSED".format(TestRunner.assertions_names[result.class_name]))
            elif isinstance(result, Failed):
                print("\t ASSERTION: {}\n\t\tFAILED: EXPECTED {}\tGOT {}".format(
                    TestRunner.assertions_names[result.class_name], result.expected, result.actual))
            elif isinstance(result, Error):
                print("\t {}\n\t\tERROR: {}".format(
                    TestRunner.assertions_names[result.class_name], result.error))
            else:
                print("\t ASSERTION: {}\n\t\tUNKNOWN RESULT".format(
                    TestRunner.assertions_names[result.class_name]))

    def run(self, test_lines):
        for test_data in test_lines:
            test = Test()
            test.parse(test_data)

        self.print_summary()
