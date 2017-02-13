import unittest
from indor.command_classes.handle import Handle
from indor.command_classes.handle_request import CallbackResponse
from indor.test_runner import TestsRunner


class TestHandleRequest(unittest.TestCase):
    def test_adding_request_works(self):
        tests_runner = TestsRunner()
        Handle(tests_runner.result_collector).parse(
            [
                "REQUEST",
                [
                    "http://localhost:5000/user/add"
                ],
                [
                    "WAITTIME",
                    "1000"
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
        # result_collector_mock.add_request.assert_called_with(CallbackResponse(
        #     url="http://localhost:5000/user/add",
        #     waittime=1000,
        #     status=200,
        #     data={"postalcode": "50316", "username": "indor"}))