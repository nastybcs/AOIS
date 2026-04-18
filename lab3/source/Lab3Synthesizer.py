from .LogicMinimizer import LogicMinimizer

class Lab3Synthesizer:
    def synthesize_down_counter(self) -> dict[str, str]:
        variables = ["Q2", "Q1", "Q0"]
        terms = {"T2": [], "T1": [], "T0": []}

        for state in range(8):
            
            q2, q1, q0 = (state >> 2) & 1, (state >> 1) & 1, state & 1

            
            next_state = (state - 1) % 8
            nq2, nq1, nq0 = (next_state >> 2) & 1, (next_state >> 1) & 1, next_state & 1

            combo = (q2, q1, q0)
            
            if q2 != nq2: terms["T2"].append(combo)
            if q1 != nq1: terms["T1"].append(combo)
            if q0 != nq0: terms["T0"].append(combo)

        minimized_expressions = {}
        for t_var, on_terms in terms.items():
            minimizer = LogicMinimizer(1, on_terms, 3)
            minimized_expressions[t_var] = minimizer.get_minimized_str(variables)

        return minimized_expressions