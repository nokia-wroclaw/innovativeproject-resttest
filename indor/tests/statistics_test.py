import unittest
import datetime

from behavioral_test import run_indor
from statistics import Statistics


class StatisticsTest(unittest.TestCase):
    def test_simple_query(self):
        statistics = Statistics()
        statistics.set_tests_start()

        test = """
            GET
                http://httpbin.org/redirect/2,
            ALLOW REDIRECTS.
            ASSERT RESPONSE STATUS Ok.
            ASSERT RESPONSE STATUS 500.
            ASSERT RESPONSE STATUS sss.
            ASSERT RESPONSE REDIRECTS COUNT = 2.
        """
        result = run_indor(test)

        statistics.set_tests_finished()
        statistics.collect_statistics(result)

        self.assertEqual(statistics.scenarios_count, 1)
        self.assertEqual(statistics.tests_count, 1)
        self.assertEqual(statistics.assertions_count, 4)
        self.assertEqual(statistics.failed_count, 1)
        self.assertEqual(statistics.passed_count, 2)
        self.assertEqual(statistics.errors_count, 1)
        self.assertGreater(statistics.get_tests_time(), datetime.timedelta())

    def test_exceptions(self):
        statistics = Statistics()

        self.assertRaises(Exception, statistics.set_tests_finished)
        self.assertRaises(Exception, statistics.get_tests_time)