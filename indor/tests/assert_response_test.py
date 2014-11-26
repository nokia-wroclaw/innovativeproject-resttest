import unittest
import mock
import src.asserts
import src.result_collector


class AssertResponseTest(unittest.TestCase):

    @mock.patch('src.test_runner.TestRunner')
    # Ustalalismy, ze metody powinny miec zdecydowanie krotsze nazwy!
    # Zeby bylo jasne co sie dzieje, proponuje pisac komentarze w testach
    def test_path_empty_then_added_response_with_error(self, mock_test_runner):
        src.result_collector.ResultCollector(mock_test_runner)
        src.asserts.AssertResponse().parse([])
        self.assertTrue(mock_test_runner.tested_classes.append.called)