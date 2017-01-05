import indor.input_parser as parser
from indor import test_runner


def run_indor(data):
    test_data = parser.parse(data)
    runner = test_runner.TestsRunner()
    return runner.run(test_data)