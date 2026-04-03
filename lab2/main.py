from core.parser import ExpressionParser
from models.boolean_function import BooleanFunction
from models.analyzer import PostAnalyzer
from algorithms.minimization import Minimizer

def main():
    expr_str = input("Введите формулу (напр. !(a & b) | c): ")
    parser = ExpressionParser(expr_str)
    func = BooleanFunction(parser)
    print(f"\nТаблица истинности для {func.variables} переменных:")
    func.print_table()
    print(f"\nВектор функции: {''.join(map(str, func.vector))}")
    print("\n[Результаты анализа]")
    print(f"СДНФ: {func.get_sdnf()}")
    print(f"СКНФ: {func.get_sknf()}")
    print(f"Числовая форма СДНФ: ({', '.join(str(i) for i, v in enumerate(func.vector) if v == 1)})")
    print(f"Числовая форма СКНФ: ({', '.join(str(i) for i, v in enumerate(func.vector) if v == 0)})")
    print(f"Индексная форма: {func.get_index_form()} (вектор: {''.join(map(str, func.vector))})")
    analyzer = PostAnalyzer(func.vector, func.variables)
    print("\n" + "="*40)
    print(" АНАЛИЗ ПО КЛАССАМ ПОСТА ")
    print("="*40)
    print(f"T0: {'+' if analyzer.check_t0() else '-'}")
    print(f"T1: {'+' if analyzer.check_t1() else '-'}")
    print(f"S:  {'+' if analyzer.check_s() else '-'}")
    print(f"M:  {'+' if analyzer.check_m() else '-'}")
    print(f"L:  {'+' if analyzer.check_l() else '-'}")
    print("\n[Полином Жегалкина]")
    print(f"P = {analyzer.get_zhegalkin_string()}")
    print("\n[Существенность переменных]")
    importance = analyzer.get_essential_variables()
    for var, essential in importance.items():
        status = "СУЩЕСТВЕННАЯ" if essential else "фиктивная"
        print(f"  Переменная {var}: {status}")
        analyzer = PostAnalyzer(func.vector, func.variables)
    print("\n[9. Булева дифференциация]")
    target_vars_input = input("Введите переменные для производной через запятую (напр. a,b): ")
    target_vars = [v.strip() for v in target_vars_input.split(',') if v.strip()]
    current_vec = func.vector
    current_vars = func.variables
    print(f"Исходный вектор: {current_vec}")
    for var in target_vars:
        if var in current_vars:
            current_vec, current_vars = analyzer.get_derivative(current_vec, current_vars, var)
            print(f"Производная по {var}:")
            print(f"  Новый вектор: {current_vec}")
            print(f"  Оставшиеся переменные: {current_vars}")
        else:
            print(f"Ошибка: переменная {var} не найдена в функции!")
    print(f"\nИТОГОВАЯ СДНФ ПРОИЗВОДНОЙ: {analyzer.vector_to_sdnf(current_vec, current_vars)}")
    minz = Minimizer(func.vector, func.variables)
    minz.method_calculation(mode='DNF')
    minz.method_table_calc(mode='DNF')
    minz.method_calculation(mode='KNF')
    minz.method_table_calc(mode='KNF')
    minz.method_karnaugh()

if __name__ == "__main__":
    main()