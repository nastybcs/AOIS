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
        print(f"\n>>> РАСЧЕТНЫЙ ({mode})")
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
        print(f"\n РАСЧЕТНО-ТАБЛИЧНЫЙ ({mode})")
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
    def method_karnaugh(self):
        def gray_code(n):
            if n == 0:
                return ['']
            prev = gray_code(n - 1)
            return ['0' + x for x in prev] + ['1' + x for x in reversed(prev)]

        def differ_by_one_bit(a, b):
            return sum(x != y for x, y in zip(a, b)) == 1

        def merge_terms(a, b):
            return ''.join([x if x == y else '-' for x, y in zip(a, b)])

        def term_covers(term, bits):
            return all(t == b or t == '-' for t, b in zip(term, bits))

        def minimize(target_value):
            terms = []
            for i, v in enumerate(self.vector):
                if v == target_value:
                    terms.append(format(i, f'0{n}b'))

            if not terms:
                return "0" if target_value == 1 else "1"

            groups = {}
            for t in terms:
                groups.setdefault(t.count('1'), []).append(t)

            prime_implicants = set()

            while groups:
                new_groups = {}
                used = set()

                keys = sorted(groups.keys())
                for i in range(len(keys) - 1):
                    for a in groups[keys[i]]:
                        for b in groups[keys[i + 1]]:
                            if differ_by_one_bit(a, b):
                                merged = merge_terms(a, b)
                                new_groups.setdefault(merged.count('1'), []).append(merged)
                                used.add(a)
                                used.add(b)

                for group in groups.values():
                    for term in group:
                        if term not in used:
                            prime_implicants.add(term)

                groups = {}
                for k, v in new_groups.items():
                    groups[k] = list(set(v))

            coverage = {t: [] for t in terms}
            for pi in prime_implicants:
                for t in terms:
                    if term_covers(pi, t):
                        coverage[t].append(pi)

            essential = set()
            for t, pis in coverage.items():
                if len(pis) == 1:
                    essential.add(pis[0])

            covered = set()
            for pi in essential:
                for t in terms:
                    if term_covers(pi, t):
                        covered.add(t)

            remaining = set(terms) - covered

            for pi in prime_implicants:
                if remaining:
                    covers = [t for t in remaining if term_covers(pi, t)]
                    if covers:
                        essential.add(pi)
                        for t in covers:
                            remaining.remove(t)

            def term_to_expr(term, is_dnf):
                parts = []
                for i, ch in enumerate(term):
                    if ch == '-':
                        continue
                    var = self.variables[i]

                    if is_dnf:
                        parts.append(var if ch == '1' else f"!{var}")
                    else:
                        parts.append(var if ch == '0' else f"!{var}")

                if not parts:
                    return "1"

                if is_dnf:
                    return "&".join(parts)
                else:
                    return "(" + " | ".join(parts) + ")"

            if target_value == 1:
                return " | ".join(f"({term_to_expr(t, True)})" for t in essential)
            else:
                return " & ".join(term_to_expr(t, False) for t in essential)

        n = len(self.variables)

        if n < 2 or n > 5:
            print("Карта Карно: поддержка 2–5 переменных")
            return

        print("\n" + "="*40)
        print(" КАРТА КАРНО ")
        print("="*40)

        
        if n == 5:
            row_vars = self.variables[:2]
            col_vars = self.variables[2:4]
            extra_var = self.variables[4]
        else:
            row_vars = self.variables[:n//2]
            col_vars = self.variables[n//2:]
            extra_var = None

        row_gray = gray_code(len(row_vars))
        col_gray = gray_code(len(col_vars))

        def get_value(bits):
            return self.vector[int(bits, 2)]

        
        if not extra_var:
            print("    ", "  ".join(col_gray))
            for r in row_gray:
                row = []
                for c in col_gray:
                    val = get_value(r + c)
                    row.append(str(val))
                print(f"{r} |  " + "  ".join(row))
        else:
            for e in ['0', '1']:
                print(f"\nСлой {extra_var} = {e}")
                print("    ", "  ".join(col_gray))
                for r in row_gray:
                    row = []
                    for c in col_gray:
                        val = get_value(r + c + e)
                        row.append(str(val))
                    print(f"{r} |  " + "  ".join(row))

        
        dnf = minimize(1)
        knf = minimize(0)

        print("\n" + "-"*40)
        print(" РЕЗУЛЬТАТ МИНИМИЗАЦИИ КАРНО")
        print("-"*40)

        print(f"Минимальная ДНФ: {dnf}")
        print(f"Минимальная КНФ: {knf}")