__author__ = 'Damian Mirecki'

import unittest
import asserts
from indor_exceptions import InvalidRelationalOperator


class TestExtractRelationalOperator(unittest.TestCase):
    def test_valid_operators(self):
        self.assertEqual("<", asserts.extract_relational_operator(" < "))
        self.assertEqual(">=", asserts.extract_relational_operator(">="))
        self.assertEqual("==", asserts.extract_relational_operator("="))

    def test_invalid_operator_raise_exception(self):
        self.assertRaises(InvalidRelationalOperator, asserts.extract_relational_operator, "bad")