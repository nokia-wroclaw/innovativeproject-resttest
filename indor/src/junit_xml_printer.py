import junit_xml
from result import Passed, Failed, Error


class JunitXMlPrinter:
    def __init__(self, scenarios_results):
        self.scenarios_results = scenarios_results

    def print_summary(self):
        test_suites = []
        for scenario_result in self.scenarios_results:
            test_suite = junit_xml.TestSuite(scenario_result.name)
            for test_result in scenario_result.test_results:
                test_case = junit_xml.TestCase(test_result.name, test_result.name)
                for result in test_result.results:
                    if isinstance(result, Failed):
                        test_case.add_failure_info("ASSERTION {} failed".format(result.pretty_name),
                                                   "EXPECTED {}\nGOT {}".format(result.expected,
                                                                                result.actual))
                    elif isinstance(result, Error):
                        test_case.add_error_info("ASSERTION {} failed".format(result.pretty_name),
                                                 "ERROR {}".format(result.error))
                    elif isinstance(result, Passed):
                        pass
                    # TODO: What to do below?
                    else:
                        raise Exception("Unknown state")
                test_suite.test_cases.append(test_case)
            test_suites.append(test_suite)
        print(junit_xml.TestSuite.to_xml_string(test_suites))