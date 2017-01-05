import indor.src.input_parser as parser
import indor.src.test_runner

__author__ = 'Sławomir Domagała'


def run_indor(data):
    test_data = parser.parse(data)
    runner = indor.src.test_runner.TestsRunner()
    return runner.run(test_data)