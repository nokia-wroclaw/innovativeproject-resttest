import os
import unittest

from indor.indor_exceptions import EnvironmentVariableNotDefined
from indor.scenario_results import ScenarioResults
from indor.result import Passed, Error, Failed
from ..common import run_indor


class TestEnvironmentVariables(unittest.TestCase):
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

    def test_env_variable_is_set(self):
        test = """
            GET #URL# .
            ASSERT RESPONSE STATUS 200.
        """

        os.environ["URL"] = "http://httpbin.org/"

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]
        self.assertEqual(1, len(scenario.test_results))

        results = scenario.test_results[0].results
        self.assertAllPassed(results)

    def test_env_variable_is_unset(self):
        test = """
            GET #RANDOM_NAME# .
            ASSERT RESPONSE STATUS 200.
        """

        try:
            result = run_indor(test)
            self.assertTrue(False, "It should throw an exception")
        except EnvironmentVariableNotDefined as e:
            self.assertEqual("RANDOM_NAME", e.args[0])

