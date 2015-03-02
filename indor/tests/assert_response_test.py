import unittest
from command_response import CommandResponse
import indor_exceptions

import mock


class AssertResponseTest(unittest.TestCase):

    @mock.patch('src.result_collector.ResultCollector')
    def test_path_empty_then_added_response_with_error(self, result_collector_mock):
        with self.assertRaises(Exception):
            CommandResponse(result_collector_mock).parse([])

    @mock.patch('src.result_collector.ResultCollector')
    def test_path_incorrect_then_added_response_with_error(self, result_collector_mock):
        with self.assertRaises(Exception):
            CommandResponse(result_collector_mock).parse(["JasIMalgosia"])