
from .tokens import Tokens

class ExpressionParser:
    def __init__(self, raw_expression: str):
        
        self.raw_expression = raw_expression.replace(" ", "")
        self.tokens = self._tokenize(self.raw_expression)
        self.postfix = self._shunting_yard(self.tokens)

    def _tokenize(self, expr: str):
        tokens = []
        i = 0
        while i < len(expr):
            char = expr[i]
            if char == '-' and i + 1 < len(expr) and expr[i+1] == '>':
                tokens.append('->')
                i += 2  
                continue
            if char in Tokens.OPERATORS or char in ('(', ')'):
                tokens.append(char)
            elif char in Tokens.VARIABLES:
                tokens.append(char)
            i += 1
        return tokens

    def _shunting_yard(self, tokens):
        
        output = []
        stack = []
        for token in tokens:
            if token in Tokens.VARIABLES:
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack: 
                    stack.pop()
            elif token in Tokens.OPERATORS:
                while (stack and stack[-1] != '(' and 
                       Tokens.PRIORITY.get(stack[-1], 0) >= Tokens.PRIORITY[token]):
                    output.append(stack.pop())
                stack.append(token)
        while stack:
            output.append(stack.pop())
        return output

    def evaluate(self, var_values: dict):
        
        stack = []
        for token in self.postfix:
            if token in Tokens.VARIABLES:
                stack.append(var_values[token])
            elif token == '!':
                stack.append(not stack.pop())
            else:
                v2 = stack.pop()
                v1 = stack.pop()
                if token == '&': 
                    stack.append(v1 and v2)
                elif token == '|': 
                    stack.append(v1 or v2)
                elif token == '->': 
                    stack.append((not v1) or v2)
                elif token == '~': 
                    stack.append(v1 == v2)
        return int(stack[0])