import unittest
import mock

from indor.command_classes.command_response import CommandResponse


class AssertResponseTest(unittest.TestCase):

    @mock.patch('indor.result_collector.ResultCollector')
    def test_path_empty_then_added_response_with_error(self, result_collector_mock):
        with self.assertRaises(Exception):
            CommandResponse(result_collector_mock).parse([])

    @mock.patch('indor.result_collector.ResultCollector')
    def test_path_incorrect_then_added_response_with_error(self, result_collector_mock):
        with self.assertRaises(Exception):
            CommandResponse(result_collector_mock).parse(["JasIMalgosia"])