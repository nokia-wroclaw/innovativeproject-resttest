import unittest

from indor import indor_exceptions
from indor.command_classes.handle import Handle
from indor.command_classes.handle_request import CallbackResponse
from indor.test_runner import TestsRunner


class TestHandleRequest(unittest.TestCase):
    def setUp(self):
        self.tests_runner = TestsRunner()
        self.result_collector = self.tests_runner.result_collector

    def test_adding_request_with_missing_url(self):
        with self.assertRaises(indor_exceptions.URLNotFound):
            Handle(self.result_collector).parse(
                [
                    [
                        "HANDLE",
                        "REQUEST",
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

    def test_adding_empty_request(self):
        callback_url = "http://localhost:5000/user/add"
        Handle(self.result_collector).parse(
            [
                "HANDLE",
                "REQUEST",
                callback_url
            ])

        expected = CallbackResponse(url=("%s" % callback_url), waittime=10.0, status="200",
                                    data=None)
        self.assertEqual(5000, self.result_collector.clb_handler_params.port)
        self.assertEqual("localhost", self.result_collector.clb_handler_params.hostname)
        self.assertEqual(expected, self.result_collector.clb_handler_params.responses[callback_url])

    def test_adding_filled_request(self):
        callback_url = "http://localhost:5000/user/add"
        Handle(self.result_collector).parse(
            [
                [
                    "HANDLE",
                    "REQUEST",
                    callback_url
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

        expected = CallbackResponse(url=callback_url, waittime=2.0, status="200",
                                    data={"postalcode": "50316", "username": "indor"})
        self.assertEqual(5000, self.result_collector.clb_handler_params.port)
        self.assertEqual("localhost", self.result_collector.clb_handler_params.hostname)
        self.assertEqual(expected, self.result_collector.clb_handler_params.responses[callback_url])
