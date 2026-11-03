import re

def evaluate(expr: str) -> int:
    expr = expr.replace(' ', '')

    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            values.append(int(left / right))

    def greater_precedence(op1, op2):
        return op1 in '+-' and op2 in '*/' or (op1 in '*/' and op2 in '*/')
    operators = []
    values = []
    i = 0
    while i < len(expr):
        if expr[i].isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            values.append(int(expr[i:j]))
            i = j - 1
        elif expr[i] in '+-*/':
            while operators and operators[-1] != '(' and greater_precedence(operators[-1], expr[i]):
                apply_operator(operators, values)
            operators.append(expr[i])
        elif expr[i] == '(':
            operators.append(expr[i])
        elif expr[i] == ')':
            while operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()
        i += 1
    while operators:
        apply_operator(operators, values)
    return values[0]