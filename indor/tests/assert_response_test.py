import unittest
import indor_exceptions

import mock

import src.asserts
import src.result_collector
import src.result


class AssertResponseTest(unittest.TestCase):

    @mock.patch('src.result_collector.ResultCollector')
    def test_path_empty_then_added_response_with_error(self, result_collector_mock):
        with self.assertRaises(Exception):
            src.asserts.AssertResponse(result_collector_mock).parse([])

    @mock.patch('src.result_collector.ResultCollector')
    def test_path_incorrect_then_added_response_with_error(self, result_collector_mock):
        with self.assertRaises(Exception):
            src.asserts.AssertResponse(result_collector_mock).parse(["JasIMalgosia"])