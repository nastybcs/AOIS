import unittest
from algorithms.minimization import Minimizer

class TestMinimizerFull(unittest.TestCase):
    def test_calculation_method_basic(self):
        vec = [0, 1, 1, 1]
        m = Minimizer(vec, ['a', 'b'])
        res = m.method_calculation()
        self.assertIn("a", res)
        self.assertIn("b", res)

    def test_table_calc_with_core(self):
        vec = [0, 0, 0, 1, 0, 1, 1, 1]
        m = Minimizer(vec, ['a', 'b', 'c'])
        res = m.method_table_calc()
        self.assertTrue("ab" in res or "ba" in res)
        self.assertTrue("bc" in res or "cb" in res)

    def test_karnaugh_3_and_4_vars(self):
        vec3 = [0, 1, 0, 1, 0, 1, 0, 1]
        m3 = Minimizer(vec3, ['a', 'b', 'c'])
        m3.method_karnaugh() 
        vec4 = [1] * 16
        m4 = Minimizer(vec4, ['a', 'b', 'c', 'd'])
        m4.method_karnaugh() 

    def test_karnaugh_invalid_vars(self):
        vec = [0] * 32
        m = Minimizer(vec, ['a', 'b', 'c', 'd', 'e'])
        m.method_karnaugh() 

    def test_const_one_and_zero(self):
        m_one = Minimizer([1, 1], ['a'])
        res = m_one.method_calculation()
        self.assertEqual(res, "1")
        m_zero = Minimizer([0, 0], ['a'])
        res_zero = m_zero.method_table_calc()
        self.assertEqual(res_zero, "") 

    def test_term_to_str_logic(self):
        m = Minimizer([1, 1, 1, 1], ['x', 'y'])
        self.assertEqual(m.term_to_str("10"), "x!y")
        self.assertEqual(m.term_to_str("01"), "!xy")
        self.assertEqual(m.term_to_str("--"), "1")
    def test_knf_minimization(self):
        vector = [0, 1, 1, 1]
        m = Minimizer(vector, ['a', 'b'])
        res = m.method_table_calc(mode='KNF')
        self.assertEqual(res, "(a+b)")

    def test_dnf_minimization(self):
        vector = [0, 1, 1, 1]
        m = Minimizer(vector, ['a', 'b'])
        res = m.method_table_calc(mode='DNF')
        self.assertTrue("a" in res and "b" in res)

if __name__ == '__main__':
    unittest.main()