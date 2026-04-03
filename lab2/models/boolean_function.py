class BooleanFunction:
    def __init__(self, parser):
        self.parser = parser
        self.variables = sorted(list(set(t for t in parser.tokens if t.isalpha())))
        self.n = len(self.variables)
        self.size = 2**self.n
        self.table = []
        self.vector = []
        self._generate_table()

    def _generate_table(self):
        for i in range(self.size):
            binary_str = f"{i:0{self.n}b}"
            var_values = {
                self.variables[j]: int(binary_str[j]) 
                for j in range(self.n)
            }
            result = self.parser.evaluate(var_values)
            row = var_values.copy()
            row['result'] = result
            self.table.append(row)
            self.vector.append(result)

    def get_sdnf(self):
        clauses = []
        for row in self.table:
            if row['result'] == 1:
                parts = []
                for v in self.variables:
                    parts.append(v if row[v] == 1 else f"!{v}")
                clauses.append(f"({' & '.join(parts)})")
        return " | ".join(clauses) if clauses else "0"

    def get_sknf(self):
        clauses = []
        for row in self.table:
            if row['result'] == 0:
                parts = []
                for v in self.variables:
                    parts.append(v if row[v] == 0 else f"!{v}")
                clauses.append(f"({' | '.join(parts)})")
        return " & ".join(clauses) if clauses else "1"

    def get_numeric_sdnf(self):
        indices = [i for i, val in enumerate(self.vector) if val == 1]
        return f"Σ({', '.join(map(str, indices))})"

    def get_numeric_sknf(self):
        indices = [i for i, val in enumerate(self.vector) if val == 0]
        return f"Π({', '.join(map(str, indices))})"

    def get_index_form(self):
        vector_str = "".join(map(str, self.vector))
        return int(vector_str, 2)

    def print_table(self):
        header = " | ".join(self.variables) + " | F"
        print(header)
        print("-" * len(header))
        for row in self.table:
            vals = [str(row[v]) for v in self.variables]
            print(f" {' | '.join(vals)} | {row['result']}")