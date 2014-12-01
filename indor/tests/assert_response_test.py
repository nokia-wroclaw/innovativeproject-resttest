import unittest
import mock
import src.asserts
import src.result_collector
import src.result


class AssertResponseTest(unittest.TestCase):

    @mock.patch('src.result_collector.ResultCollector')
    def test_path_empty_then_added_response_with_error(self, result_collector_mock):
        src.asserts.AssertResponse(result_collector_mock).parse([])
        self.assertTrue(result_collector_mock.add_result.called)
        self.assertEqual(1, len(result_collector_mock.add_result.call_args_list))
        print(result_collector_mock.add_result.call_args_list[0][0][0].__class__)
        self.assertTrue(isinstance(result_collector_mock.add_result.call_args_list[0][0][0],
                                   src.result.Error))

    @mock.patch('src.result_collector.ResultCollector')
    def test_path_incorrect_then_added_response_with_error(self, result_collector_mock):
        src.asserts.AssertResponse(result_collector_mock).parse(["JasIMalgosia"])
        self.assertTrue(result_collector_mock.add_result.called)
        self.assertEqual(1, len(result_collector_mock.add_result.call_args_list))
        print(result_collector_mock.add_result.call_args_list[0][0][0].__class__)
        self.assertTrue(isinstance(result_collector_mock.add_result.call_args_list[0][0][0], src.result.Error))