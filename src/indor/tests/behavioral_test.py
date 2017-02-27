import ast
import unittest
from threading import Timer

import requests

from indor.result_collector import ScenarioResults
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

    def getResponseForUrl(self, url):
        func = getattr(requests, "GET".lower())
        resp = func(url=url, allow_redirects=False)
        self.status_code = resp.status_code
        self.content = resp.text

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

    def test_callback_ok(self):
        test = """
            HANDLE REQUEST
                http://localhost:5000/user/add,
            WAITTIME
                10000,
            STATUS
                200,
            DATA
                postalcode 41800
                username indoor.

            POST
                http://httpbin.org/post.
            ASSERT RESPONSE STATUS OK.
            ASSERT REQUEST http://localhost:5000/user/add METHOD GET.
        """

        timer = Timer(1, lambda: self.getResponseForUrl("http://localhost:5000/user/add"))
        timer.start()
        result = run_indor(test)

        self.assertEqual(200, self.status_code)
        self.assertEqual({'postalcode': '41800', 'username': 'indoor'}, ast.literal_eval(self.content))

        self.assertScenarioCount(1, result)
        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(3, len(results))
        self.assertAllPassed(results)

    def test_many_callbacks_ok(self):
        test = """
            HANDLE REQUEST http://localhost:5000/user/add.
            HANDLE REQUEST http://localhost:5000/user/get.
            HANDLE REQUEST http://localhost:5000/user/remove.

            POST
                http://httpbin.org/post.
            ASSERT RESPONSE STATUS OK.
        """

        timer1 = Timer(1, lambda: self.getResponseForUrl("http://localhost:5000/user/add"))
        timer2 = Timer(1, lambda: self.getResponseForUrl("http://localhost:5000/user/get"))
        timer3 = Timer(1, lambda: self.getResponseForUrl("http://localhost:5000/user/remove"))
        timer1.start()
        timer2.start()
        timer3.start()
        result = run_indor(test)

        self.assertScenarioCount(1, result)
        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(4, len(results))
        self.assertAllPassed(results)

    def test_callback_not_ok(self):
        test = """
            HANDLE REQUEST
                http://localhost:5000/user/add,
            WAITTIME
                2000.
            HANDLE REQUEST
                http://localhost:5000/user/get,
            WAITTIME
                2000.
            HANDLE REQUEST
                http://localhost:5000/user/remove,
            WAITTIME
                2000.

            POST
                http://httpbin.org/post.
        """
        timer1 = Timer(1, lambda: self.getResponseForUrl("http://localhost:5000/user/add"))
        timer2 = Timer(4, lambda: self.getResponseForUrl("http://localhost:5000/user/get"))
        timer1.start()
        timer2.start()
        result = run_indor(test)
        timer1.join()
        timer2.join()

        self.assertScenarioCount(1, result)
        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(3, len(results))

        self.assertIsInstance(next(filter(lambda x: "/user/add" in x.expected, results)), Passed)
        self.assertIsInstance(next(filter(lambda x: "/user/remove" in x.expected, results)), Failed)
        self.assertIsInstance(next(filter(lambda x: "/user/get" in x.expected, results)), Failed)

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

