import input_parser as parser
import test_runner

__author__ = 'Sławomir Domagała'


def run_indor(data):
    test_data = parser.parse(data)
    runner = test_runner.TestsRunner()
    return runner.run(test_data)