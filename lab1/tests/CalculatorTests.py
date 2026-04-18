import unittest
from core.calculator import Calculator
from core.bit_number import BinaryNumber

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    
    def test_add_integers(self):
        n1 = BinaryNumber(10)
        n2 = BinaryNumber(5)
        res = self.calc.add(n1, n2)
        self.assertEqual(self.calc.complement_to_int(res), 15)

    def test_subtract_integers(self):
        n1 = BinaryNumber(10)
        n2 = BinaryNumber(7)
        res = self.calc.subtract(n1, n2)
        self.assertEqual(self.calc.complement_to_int(res), 3)

    def test_multiply_integers(self):
        n1 = BinaryNumber(6)
        n2 = BinaryNumber(7)
        res = self.calc.multiply(n1, n2)
        self.assertEqual(res[0], 0) 
        self.assertEqual(self.calc.bits_to_int_unsigned(res[1:]), 42)
    def test_multiply_integers_minus(self):
        n1 = BinaryNumber(6)
        n2 = BinaryNumber(-7)
        res = self.calc.multiply(n1, n2)
        self.assertEqual(res[0], 1) 
        self.assertEqual(self.calc.bits_to_int_unsigned(res[1:]), 42)

    def test_divide_integers(self):
        n1 = BinaryNumber(13)
        n2 = BinaryNumber(4)
        sign, q_int, q_frac = self.calc.divide(n1, n2)
        self.assertEqual(self.calc.bits_to_int_unsigned(q_int), 3)
        self.assertEqual(q_frac[0:2], [0, 1]) 

    def test_divide_by_zero(self):
        n1 = BinaryNumber(10)
        n2 = BinaryNumber(0)
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(n1, n2)

    
    def test_gray_conversions(self):
        
        bits = [0, 1, 0, 1]
        gray = self.calc.bin_tetrad_to_gray(bits)
        self.assertEqual(gray, [0, 1, 1, 1])
        bin_back = self.calc.gray_tetrad_to_bin(gray)
        self.assertEqual(bin_back, bits)

    def test_bcd_add_signed(self):
        
        t1 = [self.calc.int_to_bits_4bit(1), self.calc.int_to_bits_4bit(5)]
        t2 = [self.calc.int_to_bits_4bit(0), self.calc.int_to_bits_4bit(7)]
        sign, res = self.calc.bcd_add_signed(0, t1, 0, t2)
        self.assertEqual(self.calc.bcd_to_int(res), 22)

    def test_bcd_subtract_negative(self):
        
        t1 = [self.calc.int_to_bits_4bit(1), self.calc.int_to_bits_4bit(0)]
        t2 = [self.calc.int_to_bits_4bit(2), self.calc.int_to_bits_4bit(5)]
        sign, res = self.calc.bcd_add_signed(0, t1, 1, t2)
        self.assertEqual(sign, 1)
        self.assertEqual(self.calc.bcd_to_int(res), 15)

    
    def test_float_to_ieee_and_back(self):
        val = 12.5
        bits = self.calc.float_to_ieee754(val)
        res = self.calc.ieee754_to_float(bits)
        self.assertEqual(res, 12.5)

    def test_float_add(self):
        f1 = self.calc.float_to_ieee754(0.5)
        f2 = self.calc.float_to_ieee754(0.25)
        res_bits = self.calc.operate_floats(f1, f2, subtract=False)
        self.assertEqual(self.calc.ieee754_to_float(res_bits), 0.75)
    def test_float_substract(self):
        f1 = self.calc.float_to_ieee754(0.5)
        f2 = self.calc.float_to_ieee754(0.25)
        res_bits = self.calc.operate_floats(f1, f2, subtract=True)
        self.assertEqual(self.calc.ieee754_to_float(res_bits), 0.25)

    def test_float_multiply(self):
        f1 = self.calc.float_to_ieee754(2.5)
        f2 = self.calc.float_to_ieee754(2.0)
        res_bits = self.calc.multiply_floats(f1, f2)
        self.assertEqual(self.calc.ieee754_to_float(res_bits), 5.0)

    def test_float_divide(self):
        f1 = self.calc.float_to_ieee754(10.0)
        f2 = self.calc.float_to_ieee754(4.0)
        res_bits = self.calc.divide_floats(f1, f2)
        self.assertEqual(self.calc.ieee754_to_float(res_bits), 2.5)
    def test_float_divide_signe(self):
        f1 = self.calc.float_to_ieee754(10.0)
        f2 = self.calc.float_to_ieee754(-4.0)
        res_bits = self.calc.divide_floats(f1, f2)
        self.assertEqual(self.calc.ieee754_to_float(res_bits), -2.5)

    def test_float_zero(self):
        bits = self.calc.float_to_ieee754(0.0)
        self.assertEqual(sum(bits), 0)

    def test_float_divide_by_zero(self):
        f1 = self.calc.float_to_ieee754(1.0)
        f2 = self.calc.float_to_ieee754(0.0)
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide_floats(f1, f2)
