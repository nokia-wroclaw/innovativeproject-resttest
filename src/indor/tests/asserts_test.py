import unittest

from indor import relational_operators
from indor.indor_exceptions import InvalidRelationalOperator


class TestExtractRelationalOperator(unittest.TestCase):
    def test_valid_operators(self):
        self.assertTrue(relational_operators.compare_by_supposed_relational_operator(1, " < ", 3))
        self.assertFalse(relational_operators.compare_by_supposed_relational_operator(1, " >= ", 3))
        self.assertFalse(relational_operators.compare_by_supposed_relational_operator(1, " = ", 3))
        self.assertTrue(relational_operators.compare_by_supposed_relational_operator(1, " = ", 1))

    def test_invalid_operator_raise_exception(self):
        self.assertRaises(InvalidRelationalOperator, relational_operators.compare_by_supposed_relational_operator, 1,
                          "bad", 3)