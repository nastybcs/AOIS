from core.bit_number import BinaryNumber
from core.constants import BIT_SIZE, TETRAD_SIZE, DEGREE_VALUE, MANTISSA_SIZE
class Calculator:
    def __init__(self):
        self.size = BIT_SIZE
        self.tetrad_size = TETRAD_SIZE

    def full_add_logic(self, bits1, bits2):
        res = [0]* self.size
        carry = 0
        for i in range (self.size - 1, -1 ,-1):
            sum_val = bits1[i]+ bits2[i] + carry
            res[i] = sum_val % 2
            carry = sum_val // 2
        return res
    
    def add (self, num1: BinaryNumber, num2: BinaryNumber):
        bits1 = num1.get_complement_code()
        bits2 = num2.get_complement_code()
        return self.full_add_logic(bits1, bits2)
    
    def subtract (self, num1: BinaryNumber, num2: BinaryNumber):
        negative_bit = BinaryNumber(-num2.decimal_value)
        return self.add(num1, negative_bit)
    
    def multiply (self, num1,num2):
        bits1 = num1.get_direct_code()
        bits2 = num2.get_direct_code()
        if bits1[0] == bits2[0]:
            result_sign = 0
        else:
            result_sign = 1

        mag1 = bits1[1:]
        mag2 = bits2[1:]
        accumulated_mag = [0] * (self.size - 1)
        for i in range (len(mag2) - 1, -1, -1):
            if mag2[i] == 1:
                shift_amount = (len(mag2) -1) - i
                shifted_mag1 = self.shift_left(mag1, shift_amount)
                accumulated_mag = self.add_magnitudes(accumulated_mag,shifted_mag1)

        return [result_sign] + accumulated_mag
    def shift_left(self, bits, amount):
        if amount == 0:
            return list(bits)
        res = bits[amount:] + [0] * amount
        return res

    def add_magnitudes(self, mag1, mag2):
        size = len(mag1)
        res = [0] * size
        carry = 0
        for i in range(size - 1, -1, -1):
            sum_val = mag1[i] + mag2[i] + carry
            res[i] = sum_val % 2
            carry = sum_val // 2
        return res
    
    def divide(self, num1: BinaryNumber, num2: BinaryNumber):
        if num2.decimal_value == 0:
            raise ZeroDivisionError("Деление на ноль")
        bits1 = num1.get_direct_code()
        bits2 = num2.get_direct_code()
        if bits1[0] == bits2[0]:
            result_sign = 0
        else:
            result_sign = 1

        mag1 = bits1[1:]
        mag2 = bits2[1:]

        quotient_int = []
        current_remainder = [0] * (self.size - 1)
        for bit in mag1:
            current_remainder = current_remainder[1:] + [bit]
            rem_obj = BinaryNumber(self.bits_to_int_unsigned(current_remainder))
            div_obj = BinaryNumber(self.bits_to_int_unsigned(mag2))
            if self.bits_to_int_unsigned(current_remainder) >= self.bits_to_int_unsigned(mag2):

                sub_res_bits = self.subtract(rem_obj, div_obj) 
                new_rem_val = self.complement_to_int(sub_res_bits)
                current_remainder = self.int_to_bits_unsigned(new_rem_val)
                quotient_int.append(1)
            else:
                quotient_int.append(0)

        quotient_frac = []
        for bit in range(5):
            current_remainder = current_remainder[1:] + [0] 
            
            rem_obj = BinaryNumber(self.bits_to_int_unsigned(current_remainder))
            div_obj = BinaryNumber(self.bits_to_int_unsigned(mag2))
            
            if self.bits_to_int_unsigned(current_remainder) >= self.bits_to_int_unsigned(mag2):
                sub_res_bits = self.subtract(rem_obj, div_obj)
                new_rem_val = self.complement_to_int(sub_res_bits)
                current_remainder = self.int_to_bits_unsigned(new_rem_val)
                quotient_frac.append(1)
            else:
                quotient_frac.append(0)

        return result_sign, quotient_int, quotient_frac

    def bits_to_int_unsigned(self, bits):
        result = 0
        n = len(bits)
        power = 0
        for i in range(n - 1, -1, -1):
            if bits[i] == 1:
                result += 2 ** power
            power += 1
        return result
    def complement_to_int(self, bits):
        
        if bits[0] == 0:
            return self.bits_to_int_unsigned(bits[1:])
        
        
        
        inverted = [1 if b == 0 else 0 for b in bits]
        
        one = [0] * (len(bits) - 1) + [1]
        mag = self.full_add_logic(inverted, one)
        return -self.bits_to_int_unsigned(mag)
    def int_to_bits_unsigned(self, val):

        bits = [0] * (self.size - 1)
   
        for i in range(len(bits) - 1, -1, -1):
            bits[i] = val % 2
            val //= 2
        return bits
    def bits_to_decimal_float(self, sign_bit, int_bits, frac_bits):
    
        int_val = self.bits_to_int_unsigned(int_bits)
        frac_val = 0
        for i in range(len(frac_bits)):
            if frac_bits[i] == 1:
                frac_val += 2 ** -(i + 1)
        total = int_val + frac_val
        if sign_bit == 1:
            total = -total
        return total
    
    def gray_tetrad_to_bin(self, gray):
        bin_bits = [0] * self.tetrad_size
        bin_bits[0] = gray[0]
        for i in range (1, self.tetrad_size):
            if bin_bits[i-1] != gray[i]:
                bin_bits[i] = 1
            else:
                bin_bits[i] = 0
        return bin_bits
    def bin_tetrad_to_gray (self, bin_bits):
        gray = [0] * self.tetrad_size
        gray[0] = bin_bits[0]
        for i in range (1, self.tetrad_size):
            if bin_bits[i-1] != bin_bits[i]:
                gray[i] = 1
            else:
                gray[i] = 0
        return gray
    
    def int_to_bits_4bit(self, val):
        bits = [0] * self.tetrad_size 
        temp_value = val
        for i in range(self.tetrad_size -1, -1, -1):
            bits[i] = temp_value % 2
            temp_value //= 2
        return bits
    def int_to_bcd(self, val):
        if val == 0:
            return [[0, 0, 0, 0]]
        
        abs_val = abs(val)
        tetrads = []
        while abs_val > 0:
            digit = abs_val % 10
            tetrads.insert(0, self.int_to_bits_4bit(digit))
            abs_val //= 10
        return tetrads
    def bcd_add(self, bcd1, bcd2):
        n = max(len(bcd1), len(bcd2))
        b1 = [[0,0,0,0]] * (n - len(bcd1)) + bcd1
        b2 = [[0,0,0,0]] * (n - len(bcd2)) + bcd2

        result = []
        carry = 0
        for i in range(n - 1, -1, -1):
            d1 = self.bits_to_int_unsigned(b1[i])
            d2 = self.bits_to_int_unsigned(b2[i])
            
            s = d1 + d2 + carry
            if s >= 10:
                result.insert(0, self.int_to_bits_4bit(s - 10))
                carry = 1
            else:
                result.insert(0, self.int_to_bits_4bit(s))
                carry = 0
                
        if carry:
            result.insert(0, self.int_to_bits_4bit(carry))
        return result, carry
    def bcd_complement_to_10(self, tetrads):
        comp9 = []
        for tet in tetrads:
            digit = self.bits_to_int_unsigned(tet)
            comp9.append(self.int_to_bits_4bit(9 - digit))
    
        one = [[0,0,0,0]] * (len(tetrads) - 1) + [self.int_to_bits_4bit(1)]
        res, carry = self.bcd_add(comp9, one)
        
        if len(res) > len(tetrads):
            res = res[1:]
        return res

    def bcd_to_int(self, tetrads):
        val = 0
        for tet in tetrads:
            val = val * 10 + self.bits_to_int_unsigned(tet)
        return val
    
    def bcd_add_signed(self, sign1, tetrads1, sign2, tetrads2):
        n = max(len(tetrads1), len(tetrads2))
        t1 = [[0,0,0,0]] * (n - len(tetrads1)) + tetrads1
        t2 = [[0,0,0,0]] * (n - len(tetrads2)) + tetrads2

        if sign1 == sign2:
            res, carry = self.bcd_add(t1, t2)
            return sign1, res

        val1 = self.bcd_to_int(t1)
        val2 = self.bcd_to_int(t2)

        if val1 >= val2:
            neg_t2 = self.bcd_complement_to_10(t2)
            res, carry = self.bcd_add(t1, neg_t2)
            if len(res) > n: 
                res = res[1:]
            return sign1, res
        else:
            neg_t1 = self.bcd_complement_to_10(t1)
            res, carry = self.bcd_add(t2, neg_t1)
            if len(res) > n: 
                res = res[1:]
            return sign2, res
        
    def float_to_ieee754(self, decimal_float):
        if decimal_float == 0:
            return [0] * 32
        sign_bit = 0 if decimal_float > 0 else 1
        val = abs(decimal_float)
        exponent = 0
        if val >= 1:
            while val >= 2:
                val /= 2
                exponent += 1
        else:
            while val < 1:
                val *= 2
                exponent -= 1
        biased_exponent = exponent + DEGREE_VALUE
        exponent_bits = self._int_to_bits_unsigned_sized(biased_exponent, 8)
        mantissa_val = val - 1  
        mantissa_bits = []
        for _ in range(MANTISSA_SIZE):
            mantissa_val *= 2
            bit = int(mantissa_val)
            mantissa_bits.append(bit)
            mantissa_val -= bit

        return [sign_bit] + exponent_bits + mantissa_bits


    def operate_floats(self, f1_bits, f2_bits, subtract=False):
        s1, e1_bits, m1 = f1_bits[0], f1_bits[1:9], [1] + f1_bits[9:]
        s2, e2_bits, m2 = f2_bits[0], f2_bits[1:9], [1] + f2_bits[9:]
        if subtract:
            s2 = 1 if s2 == 0 else 0
        e1_val = self.bits_to_int_unsigned(e1_bits)
        e2_val = self.bits_to_int_unsigned(e2_bits)
        hidden_unit = 2 ** MANTISSA_SIZE
        if e1_val > e2_val:
            diff = e1_val - e2_val
            m1_int = self.bits_to_int_unsigned(m1)
            m2_int = self.bits_to_int_unsigned(m2) // (2 ** diff)
            res_exp = e1_val
        else:
            diff = e2_val - e1_val
            m1_int = self.bits_to_int_unsigned(m1) // (2 ** diff)
            m2_int = self.bits_to_int_unsigned(m2)
            res_exp = e2_val
        if s1 == s2:
            res_m_int = m1_int + m2_int
            res_sign = s1
        else:
            if m1_int >= m2_int:
                res_m_int = m1_int - m2_int
                res_sign = s1
            else:
                res_m_int = m2_int - m1_int
                res_sign = s2
        if res_m_int == 0: 
            return [0] * 32
        if res_m_int >= (hidden_unit * 2):
            while res_m_int >= (hidden_unit * 2):
                res_m_int //= 2
                res_exp += 1
        elif res_m_int < hidden_unit:
            while res_m_int < hidden_unit:
                res_m_int *= 2
                res_exp -= 1
        res_e_bits = self._int_to_bits_unsigned_sized(res_exp, 8)
        res_m_final = self._int_to_bits_unsigned_sized(res_m_int - hidden_unit, MANTISSA_SIZE)
        return [res_sign] + res_e_bits + res_m_final

    def multiply_floats(self, f1_bits, f2_bits):
    
        s1, e1_bits, m1 = f1_bits[0], f1_bits[1:9], [1] + f1_bits[9:]
        s2, e2_bits, m2 = f2_bits[0], f2_bits[1:9], [1] + f2_bits[9:]
        res_sign = 1 if s1 != s2 else 0
        res_exp = self.bits_to_int_unsigned(e1_bits) + self.bits_to_int_unsigned(e2_bits) - 127
        m1_int = self.bits_to_int_unsigned(m1)
        m2_int = self.bits_to_int_unsigned(m2)
        res_m_int = (m1_int * m2_int) // (2 ** MANTISSA_SIZE)
        hidden_unit = 2 ** MANTISSA_SIZE
        if res_m_int >= (hidden_unit * 2):
            res_m_int //= 2
            res_exp += 1
            
        res_e_bits = self._int_to_bits_unsigned_sized(res_exp, 8)
        res_m_final = self._int_to_bits_unsigned_sized(res_m_int - hidden_unit, MANTISSA_SIZE)
        return [res_sign] + res_e_bits + res_m_final

    def divide_floats(self, f1_bits, f2_bits):
        s1, e1_bits, m1 = f1_bits[0], f1_bits[1:9], [1] + f1_bits[9:]
        s2, e2_bits, m2 = f2_bits[0], f2_bits[1:9], [1] + f2_bits[9:]

        if self.bits_to_int_unsigned(e2_bits) == 0 and sum(f2_bits[9:]) == 0:
            raise ZeroDivisionError("Деление float на ноль")
        res_sign = 1 if s1 != s2 else 0
        res_exp = self.bits_to_int_unsigned(e1_bits) - self.bits_to_int_unsigned(e2_bits) + 127
        m1_int = self.bits_to_int_unsigned(m1)
        m2_int = self.bits_to_int_unsigned(m2)
        hidden_unit = 2 ** MANTISSA_SIZE
        res_m_int = (m1_int * hidden_unit) // m2_int
        
        if res_m_int < hidden_unit:
            res_m_int *= 2
            res_exp -= 1
        res_e_bits = self._int_to_bits_unsigned_sized(res_exp, 8)
        res_m_final = self._int_to_bits_unsigned_sized(res_m_int - hidden_unit, MANTISSA_SIZE)
        return [res_sign] + res_e_bits + res_m_final

    def _int_to_bits_unsigned_sized(self, val, size):
        
        bits = [0] * size
        temp = abs(val)
        for i in range(size - 1, -1, -1):
            bits[i] = temp % 2
            temp //= 2
        return bits
    def ieee754_to_float(self, bits):
        sign_bit = bits[0]
        exponent_bits = bits[1:9]
        mantissa_bits = bits[9:]
        exponent_val = self.bits_to_int_unsigned(exponent_bits) - 127
        mantissa_val = 1.0
        for i in range(len(mantissa_bits)):
            if mantissa_bits[i] == 1:
                mantissa_val += 1 / (2 ** (i + 1))
        result = ((-1) ** sign_bit) * mantissa_val * (2 ** exponent_val)
        
        return result