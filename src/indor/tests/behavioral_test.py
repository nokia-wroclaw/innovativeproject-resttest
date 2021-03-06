import unittest

from indor.scenario_results import ScenarioResults
from indor.result import Passed, Error, Failed, ConnectionError
from .common import run_indor


class TestBehavioral(unittest.TestCase):
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

    def test_no_url(self):
        test = """
            POST .
            ASSERT RESPONSE STATUS OK.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(2, len(results))
        self.assertIsInstance(results[0], ConnectionError)
        self.assertIsInstance(results[1], Error)

    def test_hello_world(self):
        test = """
            GET http://httpbin.org/ .
            ASSERT RESPONSE STATUS OK.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]
        self.assertEqual(1, len(scenario.test_results))

        results = scenario.test_results[0].results
        self.assertAllPassed(results)

    def test_basic_assertions(self):
        test = """
            # Connect
            GET http://httpbin.org/get.

            # Basic assertions on response

            ASSERT RESPONSE STATUS OK.		# Other options: Not Found, number eg. 500...
            ASSERT RESPONSE TYPE JSON.		# Other options: XML, HTML
            ASSERT RESPONSE NOT EMPTY.
            ASSERT RESPONSE LENGTH < 12345.  # Options: "=" , "<" , ">" , "<=" , ">="
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(4, len(results))
        self.assertAllPassed(results)

    def test_basic_auth(self):
        test = """
            GET
                http://httpbin.org/basic-auth/username/password,
            AUTH
                username password
                .

            ASSERT RESPONSE STATUS OK.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(1, len(results))
        self.assertAllPassed(results)

    def test_digest_auth(self):
        test = """
            GET
                http://httpbin.org/digest-auth/auth/user/pass,
            AUTH DIGEST
                user pass.

            ASSERT RESPONSE STATUS OK.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(1, len(results))
        self.assertAllPassed(results)

    def test_allow_redirects(self):
        test = """
            GET
                http://httpbin.org/redirect/2,
            ALLOW REDIRECTS.
            ASSERT RESPONSE STATUS Ok.
            ASSERT RESPONSE REDIRECTS COUNT = 2.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(2, len(results))
        self.assertAllPassed(results)

    def test_send_json(self):
        test = """
            POST
                http://httpbin.org/post,
            ALLOW REDIRECTS,
            JSON
                {
                    "name": "Joe",
                    "age": 17
                }.
            ASSERT RESPONSE STATUS OK.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(1, len(results))
        self.assertAllPassed(results)

    def test_timeout_ok(self):
        test = """
            POST
                http://httpbin.org/post,
            TIMEOUT 1000.
            ASSERT RESPONSE STATUS OK.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(1, len(results))
        self.assertAllPassed(results)

    def test_timeout_failed(self):
        test = """
            POST
                http://httpbin.org/post,
            TIMEOUT 1.
            ASSERT RESPONSE STATUS OK.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(2, len(results))
        self.assertIsInstance(results[0], ConnectionError)
        self.assertIsInstance(results[1], Error)

    def test_response_time_assertion_passed(self):
        test = """
            GET http://httpbin.org/ .
            ASSERT RESPONSE TIME < 100000.
            ASSERT RESPONSE TIME > 1.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(2, len(results))
        self.assertAllPassed(results)

    def test_response_time_assertion_failed(self):
        test = """
            GET http://httpbin.org/ .
            ASSERT RESPONSE TIME < 1.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(1, len(results))
        self.assertResultIsFailed(results[0])

    def test_invalid_response_status_code(self):
        test = """
            GET http://httpbin.org/ .
            ASSERT RESPONSE STATUS 800.
        """

        result = run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(1, len(results))
        self.assertResultIsError(results[0])

