class Minimizer:
    def __init__(self, vector, variables):
        self.vector = vector
        self.variables = variables
        self.n = len(variables)

    def get_initial_terms(self, target_value):
        return [f"{i:0{self.n}b}" for i, val in enumerate(self.vector) if val == target_value]

    def get_prime_implicants_with_steps(self, initial_terms):
        steps = []
        current = set(initial_terms)
        all_prime = set()
        step_num = 1
        while current:
            next_step = set()
            used = set()
            items = list(current)
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    diffs = [k for k in range(self.n) if items[i][k] != items[j][k]]
                    if len(diffs) == 1:
                        pos = diffs[0]
                        new_term = list(items[i])
                        new_term[pos] = '-'
                        next_step.add("".join(new_term))
                        used.add(items[i])
                        used.add(items[j])
            
            steps.append({'num': step_num, 'terms': sorted(list(current))})
            all_prime.update(current - used)
            if not next_step: 
                break
            current = next_step
            step_num += 1
        return steps, sorted(list(all_prime))

    def method_calculation(self, mode='DNF'):
        target = 1 if mode == 'DNF' else 0
        print(f"\n>>> МЕТОД 1: РАСЧЕТНЫЙ ({mode})")
        initial = self.get_initial_terms(target)
        if not initial:
            print(f"Нет наборов для {mode}")
            return "Константа"
        steps, primes = self.get_prime_implicants_with_steps(initial)
        for s in steps:
            print(f"Стадия {s['num']}: {', '.join(s['terms'])}")
        res = self.format_result(primes, mode)
        print(f"Результат ({mode}): {res}")
        return res

    def method_table_calc(self, mode='DNF'):
        target = 1 if mode == 'DNF' else 0
        print(f"\n>>> МЕТОД 2: РАСЧЕТНО-ТАБЛИЧНЫЙ ({mode})")
        initial = self.get_initial_terms(target)
        if not initial: 
            return "" 
        steps, primes = self.get_prime_implicants_with_steps(initial)
        header = " Импликанта | " + " | ".join(initial)
        print(header)
        print("-" * len(header))
        table = {}
        for p in primes:
            row_label = self.term_to_str(p, mode)
            row_display = f" {row_label:<10} |"
            matches = []
            for term in initial:
                is_match = all(p[k] == '-' or p[k] == term[k] for k in range(self.n))
                row_display += "  X  |" if is_match else "     |"
                if is_match: 
                    matches.append(term)
            table[p] = matches
            print(row_display)
        selected = set()
        covered = set()
        for term in initial:
            covers = [p for p, targets in table.items() if term in targets]
            if len(covers) == 1:
                selected.add(covers[0])
                covered.update(table[covers[0]])
        for p, targets in table.items():
            if not all(t in covered for t in initial):
                if any(t not in covered for t in targets):
                    selected.add(p)
                    covered.update(targets)
        res = self.format_result(selected, mode)
        print(f"Результат ({mode}): {res}")
        return res

    def method_karnaugh(self):
        print("\n>>> МЕТОД 3: ТАБЛИЧНЫЙ (КАРТА КАРНО)")
        gray = ["00", "01", "11", "10"]
        if self.n == 2:
            rows, cols = ["0", "1"], ["0", "1"]
            r_vars, c_vars = self.variables[:1], self.variables[1:]
        elif self.n == 3:
            rows, cols = ["0", "1"], gray
            r_vars, c_vars = self.variables[:1], self.variables[1:]
        elif self.n == 4:
            rows, cols = gray, gray
            r_vars, c_vars = self.variables[:2], self.variables[2:]
        else:
            print("Карно только для 2-4 переменных.")
            return
        print(f"Карта для: {''.join(r_vars)} \\ {''.join(c_vars)}")
        print("      " + "  ".join(cols))
        print("    " + "-" * (len(cols) * 4 + 2))
        for r in rows:
            line = f" {r} |"
            for c in cols:
                idx = int(r + c, 2)
                line += f"  {self.vector[idx]} "
            print(line)
        print("\nРезультаты минимизации по карте:")
        res_dnf = self.method_table_calc(mode='DNF')
        res_knf = self.method_table_calc(mode='KNF')
        print(f"\nИТОГОВАЯ МДНФ (по 1): {res_dnf}")
        print(f"ИТОГОВАЯ МКНФ (по 0): {res_knf}")

    def term_to_str(self, term, mode='DNF'):
        parts = []
        for i in range(self.n):
            if term[i] == '-': 
                continue
            if mode == 'DNF':
                parts.append(self.variables[i] if term[i] == '1' else f"!{self.variables[i]}")
            else:
                parts.append(self.variables[i] if term[i] == '0' else f"!{self.variables[i]}")
        if not parts: 
            return "1" if mode == 'DNF' else "0"
        if mode == 'DNF':
            return "".join(parts)
        else:
            return f"({'+'.join(parts)})"

    def format_result(self, terms, mode):
        if not terms: 
            return "0" if mode == 'DNF' else "1"
        sep = " | " if mode == 'DNF' else " & "
        formatted = sorted([self.term_to_str(t, mode) for t in terms])
        return sep.join(formatted)