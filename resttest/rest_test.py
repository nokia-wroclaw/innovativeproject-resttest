# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'
from requests.structures import CaseInsensitiveDict
from asserts import AssertResponseStatus, AssertResponseNotEmpty, \
    AssertResponseContentTypeJson, AssertResponseLengthGreater
from test import Test
from result_collector import ResultCollector

# Sławek
# TODO
# * Dlaczego tyle niepotrzebnych dziedziczeń?
# * Zrobić osobną klasę na TestRunner.assertion_names?
# * Gdzie przechwytujemy wyjątki (bo gdzie rzucamy wiadomo), np. użytkownik podał za małą liczbę argumentów albo za małą ich liczbę
# trzeba dobrze przemyśleć, żeby później w łatwy sposób komunikować to użytkownikowi
# * Dlaczego test splitujemy w linie w innym pliku?


class TestRunner:
    assertions_names = CaseInsensitiveDict()

    def __init__(self):
        self.response = None
        self.tested_classes = []  # list of all classes created in this test
        ResultCollector(self)

        TestRunner.tested_classes = []
        TestRunner.assertions_names[AssertResponseContentTypeJson.__name__] = "RESPONSE CONTENT TYPE IS JSON"
        TestRunner.assertions_names[AssertResponseLengthGreater.__name__] = "RESPONSE LENGTH GREATER"
        TestRunner.assertions_names[AssertResponseNotEmpty.__name__] = "RESPONSE NOT EMPTY"
        TestRunner.assertions_names[AssertResponseStatus.__name__] = "RESPONSE STATUS"
        TestRunner.request = None

    def print_summary(self):
        print("Tests finished")
        print("Executed tests:")
        for test in self.tested_classes:
            if test.result.status:
                print("\t ASSERTION: {}\n\t\tPASSED".format(TestRunner.assertions_names[test.__class__.__name__]))
            else:
                print("\t ASSERTION: {}\n\t\tFAILED: EXPECTED {}\tGOT {}".format(
                    TestRunner.assertions_names[test.__class__.__name__], test.result.expected, test.result.actual))

    def run_test(self, test_lines):
        for line in test_lines:
            test = Test()
            args = line.strip(".").split(" ")
            test.parse(args)

        self.print_summary()