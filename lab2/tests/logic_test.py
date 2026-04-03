import unittest
from core.parser import ExpressionParser
from models.boolean_function import BooleanFunction

class TestBooleanFunction(unittest.TestCase):
    def setUp(self):
        self.parser = ExpressionParser("a & b")
        self.func = BooleanFunction(self.parser)

    def test_table_generation(self):
        self.assertEqual(len(self.func.table), 4)
        self.assertEqual(self.func.vector, [0, 0, 0, 1])
    def test_sdnf(self):
        sdnf = self.func.get_sdnf()
        self.assertIn("a & b", sdnf)
        zero_func = BooleanFunction(ExpressionParser("a & !a"))
        self.assertEqual(zero_func.get_sdnf(), "0")

    def test_sknf(self):
        sknf = self.func.get_sknf()
        self.assertTrue(sknf.count("&") >= 2)
        one_func = BooleanFunction(ExpressionParser("a | !a"))
        self.assertEqual(one_func.get_sknf(), "1")

    def test_numeric_forms(self):
        self.assertEqual(self.func.get_numeric_sdnf(), "Σ(3)")
        self.assertEqual(self.func.get_numeric_sknf(), "Π(0, 1, 2)")

    def test_index_form(self):
        self.assertEqual(self.func.get_index_form(), 1)

    def test_print_table(self):
        try:
            self.func.print_table()
        except Exception as e:
            self.fail(f"print_table() raised {e} unexpectedly!")
