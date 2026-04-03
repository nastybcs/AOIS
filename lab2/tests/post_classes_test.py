import unittest
from models.analyzer import PostAnalyzer

class TestPostClasses(unittest.TestCase):
    
    def setUp(self):
        self.vars5 = ['a', 'b', 'c', 'd', 'e']
        self.vars3 = ['a', 'b', 'c']

    def test_const_zero(self):
        analyzer = PostAnalyzer([0]*32, self.vars5)
        self.assertTrue(analyzer.check_t0())
        self.assertFalse(analyzer.check_t1())
        self.assertTrue(analyzer.check_m())
        self.assertTrue(analyzer.check_l())
        self.assertEqual(analyzer.get_zhegalkin_string(), "0")

    def test_variable_a_3vars(self):
        vec = [0, 0, 0, 0, 1, 1, 1, 1]
        analyzer = PostAnalyzer(vec, self.vars3)
        self.assertTrue(analyzer.check_t0())
        self.assertTrue(analyzer.check_t1())
        self.assertTrue(analyzer.check_m())
        self.assertTrue(analyzer.check_l())
        self.assertEqual(analyzer.get_zhegalkin_string(), "a")

    def test_not_linear_and_zhegalkin(self):
        vars2 = ['a', 'b']
        vec = [0, 0, 0, 1]
        analyzer = PostAnalyzer(vec, vars2)
        self.assertFalse(analyzer.check_l())
        self.assertEqual(analyzer.get_zhegalkin_string(), "ab")

    def test_essential_and_fictitious(self):
        vec = [0, 0, 1, 1, 1, 1, 1, 1]
        analyzer = PostAnalyzer(vec, self.vars3)
        importance = analyzer.get_essential_variables()
        self.assertTrue(importance['a'])
        self.assertTrue(importance['b'])
        self.assertFalse(importance['c']) 

    def test_derivatives(self):
        vars2 = ['a', 'b']
        vec = [0, 1, 1, 0]
        analyzer = PostAnalyzer(vec, vars2)
        deriv_vec, deriv_vars = analyzer.get_derivative(vec, vars2, 'a')
        self.assertEqual(deriv_vec, [1, 1]) 
        self.assertEqual(deriv_vars, ['b'])
        sdnf = analyzer.vector_to_sdnf(deriv_vec, deriv_vars)
        self.assertEqual(sdnf, "1")

    def test_mixed_derivative(self):
        vars2 = ['a', 'b']
        vec = [0, 0, 0, 1]
        analyzer = PostAnalyzer(vec, vars2)
        vec_a, vars_a = analyzer.get_derivative(vec, vars2, 'a')
        vec_ab, vars_ab = analyzer.get_derivative(vec_a, vars_a, 'b')
        self.assertEqual(vec_ab, [1]) 
        self.assertEqual(len(vars_ab), 0)
