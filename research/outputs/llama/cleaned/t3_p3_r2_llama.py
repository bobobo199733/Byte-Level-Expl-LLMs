def evaluate(expr: str) -> int:

    def apply_operator():
        op = operators.pop()
        right = values.pop()
        left = values.pop()
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left // right

    def precedence(op):
        if op in {'+', '-'}:
            return 1
        if op in {'*', '/'}:
            return 2
        return 0
    i = 0
    num = ''
    values = []
    operators = []
    while i < len(expr):
        if expr[i].isspace():
            i += 1
            continue
        if expr[i].isdigit():
            while i < len(expr) and expr[i].isdigit():
                num += expr[i]
                i += 1
            values.append(int(num))
            num = ''
        elif expr[i] in {'+', '-', '*', '/'}:
            while operators and operators[-1] != '(' and (precedence(operators[-1]) >= precedence(expr[i])):
                apply_operator()
            operators.append(expr[i])
            i += 1
        elif expr[i] == '(':
            operators.append(expr[i])
            i += 1
        elif expr[i] == ')':
            while operators[-1] != '(':
                apply_operator()
            operators.pop()
            i += 1
    while operators:
        apply_operator()
    return values[0]