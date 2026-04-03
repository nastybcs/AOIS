import math

class PostAnalyzer:
    def __init__(self, vector, variables):
        self.vector = vector
        self.variables = variables
        self.size = len(vector)
        self.n = int(math.log2(self.size)) if self.size > 0 else 0
        self._coeffs = self._get_zhegalkin_coeffs()

    def check_t0(self):
        
        return self.vector[0] == 0

    def check_t1(self):
        
        return self.vector[-1] == 1

    def check_s(self):
        
        for i in range(self.size // 2):
            if self.vector[i] == self.vector[self.size - 1 - i]:
                return False
        return True

    def check_m(self):
        
        for i in range(self.size):
            for j in range(self.size):
                if (i & j) == i:  
                    if self.vector[i] > self.vector[j]:
                        return False
        return True

    def check_l(self):
        
        for i, c in enumerate(self._coeffs):
            if c == 1 and bin(i).count('1') > 1:
                return False
        return True

    def _get_zhegalkin_coeffs(self):
        
        res = list(self.vector)
        n = len(res)
        coeffs = [res[0]]
        for i in range(1, n):
            for j in range(n - 1, i - 1, -1):
                res[j] = res[j] ^ res[j-1]
            coeffs.append(res[i])
        return coeffs

    def get_zhegalkin_string(self):
        
        terms = []
        for i, c in enumerate(self._coeffs):
            if c == 1:
                if i == 0:
                    terms.append("1")
                else:
                    term_name = ""
                    bin_idx = f"{i:0{self.n}b}"
                    for j in range(self.n):
                        if bin_idx[j] == '1':
                            term_name += self.variables[j]
                    terms.append(term_name)
        return " ⊕ ".join(terms) if terms else "0"

    def get_essential_variables(self):
        
        results = {}
        for idx, var in enumerate(self.variables):
            is_essential = False
            step = 1 << (self.n - 1 - idx)
            for i in range(self.size):
                if (i & step) == 0:
                    val1 = self.vector[i]
                    val2 = self.vector[i + step]
                    if val1 != val2:
                        is_essential = True
                        break
            results[var] = is_essential
        return results
    def get_derivative(self, current_vector, current_vars, target_var):

        if target_var not in current_vars:
            return current_vector, current_vars
        idx = current_vars.index(target_var)
        n = len(current_vars)
        step = 1 << (n - 1 - idx)
        new_vector = []
        for i in range(len(current_vector)):
            if (i & step) == 0:
                val1 = current_vector[i]
                val2 = current_vector[i + step]
                new_vector.append(val1 ^ val2)
        new_vars = [v for v in current_vars if v != target_var]
        return new_vector, new_vars

    def vector_to_sdnf(self, vector, vars_list):
        
        if not any(vector): 
            return "0"
        if all(vector): 
            return "1"
        n = len(vars_list)
        clauses = []
        for i, val in enumerate(vector):
            if val == 1:
                bin_str = f"{i:0{n}b}"
                parts = []
                for j in range(n):
                    parts.append(vars_list[j] if bin_str[j] == '1' else f"!{vars_list[j]}")
                clauses.append(f"({' & '.join(parts)})")
        return " | ".join(clauses)

    
    def _get_zhegalkin_coeffs(self):
        res = list(self.vector)
        n = len(res)
        coeffs = [res[0]]
        for i in range(1, n):
            for j in range(n - 1, i - 1, -1):
                res[j] = res[j] ^ res[j-1]
            coeffs.append(res[i])
        return coeffs