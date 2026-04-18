from core.constants import BIT_SIZE
class BinaryNumber:
    def __init__(self,value: int):
        self.decimal_value = value
        self.size = BIT_SIZE

    def get_direct_code(self):
        bits = [0] * self.size
        if self.decimal_value < 0:
            bits[0] = 1
        else:
            bits[0] = 0
        temp_value = abs(self.decimal_value)
        for i in range(self.size - 1, 0, -1):
            reminder = temp_value % 2
            bits[i] = reminder
            temp_value = temp_value // 2

        return bits
    def get_reverse_code(self):
        direct = self.get_direct_code()
        if self.decimal_value >= 0:
            return direct
        reverse = [0] * self.size
        reverse[0] = direct[0]
        for i in range(1,self.size):
            if direct[i] == 0:
                reverse[i] = 1
            else:
                reverse[i] = 0
        return reverse

    def get_complement_code (self):
        if self.decimal_value >= 0:
            return self.get_direct_code()
        reverse = self.get_reverse_code()
        complement = list(reverse)
        carry = 1
        for i in range(self.size - 1, 0, -1):
            sum_bits = complement[i] + carry

            if sum_bits == 2:
                complement[i] = 0
                carry = 1
            elif sum_bits == 1:
                complement[i] = 1
                carry = 0
            else:
                complement[i] = 0
                carry = 0
        return complement
