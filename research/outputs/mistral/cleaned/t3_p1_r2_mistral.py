from functools import reduce
from operator import (add, sub, mul, truediv)
import re

def evaluate(expr):
    def _eval(precedence, ops, tokens):
        operators = set(ops)
        operators_dict = {op: getattr(reduce, op) for op in (add, sub, mul, truediv)}

        stack = []
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in operators:
                b = stack.pop()
                a = stack.pop()
                op = operators_dict[token]
                stack.append(op(a, b))
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack[-1] != '(':
                    stack.pop()
                stack.pop()

        if len(stack) != 1 or stack[0] not in (int, float):
            raise ValueError("Invalid expression")

        return stack[0]

    def _parse(expression):
        tokens = re.findall('\d+|(\+\+|-\-|\*\*|/\/)|\(|\)', expression)
        ops = set(['+', '-', '*', '/'])
        return _eval(precedence={'**': 3, '/': 2, '*': 1, '-': 1, '+': 0},
                     ops, tokens)

    try:
        return int(_parse(expr))
    except ValueError as e:
        raise ValueError("Invalid expression: {}".format(e))