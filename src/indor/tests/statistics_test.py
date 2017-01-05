import unittest
import datetime

from .common import run_indor
from indor.statistics import Statistics


class StatisticsTest(unittest.TestCase):
    def test_simple_query(self):
        statistics = Statistics()
        statistics.tests_started()

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

        statistics.tests_finished()
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

        self.assertRaises(Exception, statistics.tests_finished)
        self.assertRaises(Exception, statistics.get_tests_time)
