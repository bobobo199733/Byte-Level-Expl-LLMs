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
        else:
            return left // right
    values, operators = ([], [])
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
            continue
        if expr[i].isdigit():
            j = i
            while i < len(expr) and expr[i].isdigit():
                i += 1
            values.append(int(expr[j:i]))
        elif expr[i] == '(':
            operators.append(expr[i])
            i += 1
        elif expr[i] in '+-*/':
            while operators and operators[-1] != '(' and (operators[-1] in '+-*/') and (expr[i] == '*' or operators[-1] == '/'):
                values.append(apply_operator())
            operators.append(expr[i])
            i += 1
        else:
            raise ValueError('Invalid character')
    while operators:
        values.append(apply_operator())
    if len(values) != 1:
        raise ValueError('Invalid expression')
    return values[0]