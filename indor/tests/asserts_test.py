__author__ = 'Damian Mirecki'

import unittest
import relational_operators
from indor_exceptions import InvalidRelationalOperator


class TestExtractRelationalOperator(unittest.TestCase):
    def test_valid_operators(self):
        self.assertEqual("<", relational_operators.extract_relational_operator(" < "))
        self.assertEqual(">=", relational_operators.extract_relational_operator(">="))
        self.assertEqual("==", relational_operators.extract_relational_operator("="))

    def test_invalid_operator_raise_exception(self):
        self.assertRaises(InvalidRelationalOperator, relational_operators.extract_relational_operator, "bad")