import os
from core.calculator import Calculator
from core.bit_number import BinaryNumber

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_bits(bits):
    
    return " ".join(map(str, bits))

def print_header(text):
    print("=" * 60)
    print(f"{text:^60}")
    print("=" * 60)

def main():
    calc = Calculator()
    
    while True:
        clear_screen()
        print_header("ЛАБОРАТОРНАЯ РАБОТА: АРИФМЕТИЧЕСКИЙ КАЛЬКУЛЯТОР")
        print("1. [Пункт 1-4] Целые числа (+, -, *, /)")
        print("2. [Пункт 5]    BCD в коде Грея (+, -)")
        print("3. [Пункт 6]    Числа с плавающей точкой IEEE-754 (+, -, *, /)")
        print("0. Выход")
        print("-" * 60)
        
        choice = input("Выберите пункт меню: ")

        if choice == '1':
            clear_screen()
            print_header("ЦЕЛЫЕ ЧИСЛА (БИНАРНЫЙ ВЫВОД)")
            try:
                a = int(input("Введите число A: "))
                b = int(input("Введите число B: "))
                num1, num2 = BinaryNumber(a), BinaryNumber(b)
                
                
                add_res = calc.add(num1, num2)
                print("\n[+] Сложение:")
                print(f"Биты: {format_bits(add_res)}")
                print(f"Результат: {calc.complement_to_int(add_res)}")

                sub_res = calc.subtract(num1, num2)
                print("\n[-] Вычитание (A - B):")
                print(f"Биты: {format_bits(sub_res)}")
                print(f"Результат: {calc.complement_to_int(sub_res)}")

                
                mul_res = calc.multiply(num1, num2)
                print("\n[*] Умножение:")
                print(f"Биты: {format_bits(mul_res)}")
                print(f"Результат: {calc.bits_to_int_unsigned(mul_res[1:]) * (-1 if mul_res[0] else 1)}")
                
                
                sign, q_int, q_frac = calc.divide(num1, num2)
                print("\n[/] Деление (Знак | Целая часть | Дробная часть):")
                print(f"Биты: [{sign}] | {format_bits(q_int)} | {format_bits(q_frac)}")
                print(f"Результат: {calc.bits_to_decimal_float(sign, q_int, q_frac)}")

            except Exception as e:
                print(f"\nОшибка: {e}")
            input("\nНажмите Enter...")

        elif choice == '2':
            clear_screen()
            print_header("BCD В КОДЕ ГРЕЯ (ПОТЕТРАДНЫЙ ВЫВОД)")
            try:
                a = int(input("Введите число A (целое неотрицательное): "))
                b = int(input("Введите число B (целое неотрицательное): "))
                if a < 0 or b < 0:
                    print("Числа должны быть неотрицательными.")
                    input("\nНажмите Enter...")
                    continue
                t1 = calc.int_to_bcd(a)
                t2 = calc.int_to_bcd(b)
                g1 = [calc.bin_tetrad_to_gray(t) for t in t1]
                g2 = [calc.bin_tetrad_to_gray(t) for t in t2]
                print(f"\nЧисло A в Грей-BCD: {[''.join(map(str, g)) for g in g1]}")
                print(f"Число B в Грей-BCD: {[''.join(map(str, g)) for g in g2]}")
                res_sign, res_bin = calc.bcd_add_signed(0, t1, 0, t2)
                res_gray = [calc.bin_tetrad_to_gray(t) for t in res_bin]

                print(f"\nРезультат (BCD Грей): {'-' if res_sign else ''}{[''.join(map(str, g)) for g in res_gray]}")
                print(f"Десятичное значение: {'-' if res_sign else ''}{calc.bcd_to_int(res_bin)}")
            except Exception as e:
                print(f"Ошибка: {e}")
            input("\nНажмите Enter...")

        elif choice == '3':
            clear_screen()
            print_header("IEEE-754 (ЗНАК | ПОРЯДОК | МАНТИССА)")
            try:
                fa = float(input("Введите число A: "))
                fb = float(input("Введите число B: "))
                
                bits_a = calc.float_to_ieee754(fa)
                bits_b = calc.float_to_ieee754(fb)
                
                ops = [
                    ("Сложение", calc.operate_floats(bits_a, bits_b, False)),
                    ("Вычитание", calc.operate_floats(bits_a, bits_b, True)),
                    ("Умножение", calc.multiply_floats(bits_a, bits_b)),
                    ("Деление", calc.divide_floats(bits_a, bits_b))
                ]
                
                for name, res in ops:
                    s, exp, mant = res[0], res[1:9], res[9:]
                    print(f"\n--- {name} ---")
                    print(f"Биты: [{s}] [{' '.join(map(str, exp))}] [{' '.join(map(str, mant))}]")
                    print(f"Число: {calc.ieee754_to_float(res)}")
                    
            except Exception as e:
                print(f"Ошибка: {e}")
            input("\nНажмите Enter...")

        elif choice == '0':
            break
if __name__ == "__main__":
    main()