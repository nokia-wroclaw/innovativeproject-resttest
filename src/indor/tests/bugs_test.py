import unittest

from indor.scenario_results import ScenarioResults
from indor.result import Passed, Error, Failed
from .common import run_indor


class TestBugs(unittest.TestCase):
    def assertAllPassed(self, results):
        for result in results:
            self.assertIsInstance(result, Passed)

    def assertScenarioCount(self, count, result):
        self.assertEqual(count, len(result))
        for scenario in result:
            self.assertIsInstance(scenario, ScenarioResults)

    def assertResultIsFailed(self, obj):
        self.assertIsInstance(obj, Failed)

    def assertResultIsError(self, obj):
        self.assertIsInstance(obj, Error)

    def test_definition_of_constants_in_commented_lines_are_ignored(self):
        test = """
            # DEFINE BASE =
            DEFINE BASE = http://httpbin.org/
            GET @BASE@ .
            ASSERT RESPONSE STATUS OK.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]
        self.assertEqual(1, len(scenario.test_results))

        results = scenario.test_results[0].results
        self.assertAllPassed(results)

    def test_repeats_in_commented_lines_are_ignored(self):
        test = """
            /%
            REPEAT FOR
            {
                "run1a": {"url": "http://www.wp.pl", "expected_code": 200 },
                "run1b": {"url": "http://ww.wp.pl", "expected_code": 404 }
            }
            %/
                GET http://www.wp.pl.
                ASSERT RESPONSE STATUS 200.
            # END REPEAT
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]
        self.assertEqual(1, len(scenario.test_results))

        results = scenario.test_results[0].results
        self.assertAllPassed(results)

