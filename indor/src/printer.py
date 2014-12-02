# coding=utf-8
from requests.structures import CaseInsensitiveDict
from asserts import AssertResponseTypeJson, AssertResponseLengthGreater, AssertResponseNotEmpty, AssertResponseEmpty, \
    AssertResponseStatus, AssertResponseRedirectsCount, AssertCookieSet, AssertCookieValue, AssertPathExists, \
    AssertPathContainsAny, AssertPathContainsEach, AssertPathNodesCountEqual, AssertPathNodesCountGreater, \
    AssertPathNodesCountLess, AssertPathFinal, AssertHeaderSet, AssertHeaderValue
from connect import Connect

__author__ = 'Sławomir Domagała'
from result import Passed, Failed, Error


class Printer:
    def __init__(self, scenarios_results):
        self.scenarios_results = scenarios_results

    def print_summary(self):
        print("Execution finished")
        for scenario_result in self.scenarios_results:
            print("Scenario \"{}\" with flags: {}".format(scenario_result.name, scenario_result.flags))
            for test_result in scenario_result.test_results:
                print("\tTest {}".format(test_result.name))
                for result in test_result.results:
                    if isinstance(result, Passed):
                        print("\t\t ASSERTION: {}\n\t\tPASSED".format(Printer.assertions_names[result.class_name]))
                    elif isinstance(result, Failed):
                        print("\t\t ASSERTION: {}\n\t\tFAILED: EXPECTED {}\tGOT {}".format(
                            Printer.assertions_names[result.class_name], result.expected, result.actual))
                    elif isinstance(result, Error):
                        print("\t\t {}\n\t\tERROR: {}".format(
                            Printer.assertions_names[result.class_name], result.error))
                    else:
                        print("\t\t ASSERTION: {}\n\t\tUNKNOWN RESULT".format(
                            Printer.assertions_names[result.class_name]))

#TW: IMO to narusza DRY jak cholera
#TW: Czemu robimy to tu a nie w poszczególnych klasach? To najbrzydszy kod jaki widziałem :P
#SD: W jaki sposób to narusza DRY?
#SD: Czego klasa odpowiedzialna za testowanie ma wiedzieć, jak się użytkownikowi drukować?
Printer.assertions_names = CaseInsensitiveDict()
Printer.assertions_names[AssertResponseTypeJson.__name__] = "RESPONSE CONTENT TYPE IS JSON"
Printer.assertions_names[AssertResponseLengthGreater.__name__] = "RESPONSE LENGTH GREATER"
Printer.assertions_names[AssertResponseNotEmpty.__name__] = "RESPONSE NOT EMPTY"
Printer.assertions_names[AssertResponseEmpty.__name__] = "RESPONSE EMPTY"
Printer.assertions_names[AssertResponseStatus.__name__] = "RESPONSE STATUS"
Printer.assertions_names[AssertResponseRedirectsCount.__name__] = "RESPONSE REDIRECTS COUNT"
Printer.assertions_names[AssertCookieSet.__name__] = "COOKIE SET"
Printer.assertions_names[AssertCookieValue.__name__] = "COOKIE VALUE"
Printer.assertions_names[AssertHeaderSet.__name__] = "HEADER SET"
Printer.assertions_names[AssertHeaderValue.__name__] = "HEADER VALUE"
Printer.assertions_names[Connect.__name__] = "MAKING REQUEST"
Printer.assertions_names[AssertPathExists.__name__] = "ASSERT PATH EXISTS"
Printer.assertions_names[AssertPathContainsAny.__name__] = "ASSERT PATH CONTAINS ANY"
Printer.assertions_names[AssertPathContainsEach.__name__] = "ASSERT PATH CONTAINS EACH"
Printer.assertions_names[AssertPathNodesCountEqual.__name__] = "ASSERT PATH NODES COUNT EQUAL"
Printer.assertions_names[AssertPathNodesCountGreater.__name__] = "ASSERT PATH NODES COUNT GREATER"
Printer.assertions_names[AssertPathNodesCountLess.__name__] = "ASSERT PATH NODES COUNT LESS"
Printer.assertions_names[AssertPathFinal.__name__] = "ASSERT PATH FINAL"