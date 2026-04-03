class Tokens:
    PRIORITY = {
        '!': 5,
        '&': 4,
        '|': 3,
        '->': 2,
        '~': 1,
        '(': 0  
    }
    OPERATORS = set(PRIORITY.keys())
    VARIABLES = {'a', 'b', 'c', 'd', 'e'}