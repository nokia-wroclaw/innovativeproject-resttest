import unittest
from indor.command_classes.handle import Handle
from indor.command_classes.handle_request import CallbackResponse
from indor.test_runner import TestsRunner


class TestHandleRequest(unittest.TestCase):
    def test_adding_empty_request(self):
        tests_runner = TestsRunner()
        Handle(tests_runner.result_collector).parse(
            [
                "REQUEST",
                [
                    "http://localhost:5000/user/add"
                ]
            ])

        expected = CallbackResponse(url="http://localhost:5000/user/add", waittime=10.0, status="200",
                                    data=None)
        self.assertEqual(expected, tests_runner.result_collector.requests[0])

    def test_adding_filled_request(self):
        tests_runner = TestsRunner()
        Handle(tests_runner.result_collector).parse(
            [
                "REQUEST",
                [
                    "http://localhost:5000/user/add"
                ],
                [
                    "WAITTIME",
                    "2000"
                ],
                [
                    "STATUS",
                    "200"
                ],
                [
                    "DATA",
                    "postalcode",
                    "50316",
                    "username",
                    "indor"
                ]
            ])

        expected = CallbackResponse(url="http://localhost:5000/user/add", waittime=2.0, status="200", data={"postalcode": "50316", "username": "indor"})
        self.assertEqual(expected, tests_runner.result_collector.requests[0])