def evaluate(expr: str) -> int:

    def apply_op(operators, values):
        op = operators.pop()
        right = values.pop()
        left = values.pop()
        if op == '+':
            values.append(left + right)
        elif op == '-':
            values.append(left - right)
        elif op == '*':
            values.append(left * right)
        elif op == '/':
            values.append(int(left / right))

    def precedence(c):
        if c == '+' or c == '-':
            return 1
        if c == '*' or c == '/':
            return 2
        return 0
    operators = []
    values = []
    i = 0
    while i < len(expr):
        expr = expr.replace(' ', '')
        ch = expr[i]
        if ch.isdigit():
            j = i + 1
            while j < len(expr) and expr[j].isdigit():
                j += 1
            values.append(int(expr[i:j]))
            i = j - 1
        elif ch in '+-*/':
            while operators and operators[-1] != '(' and (precedence(operators[-1]) >= precedence(ch)):
                apply_op(operators, values)
            operators.append(ch)
        elif ch == '(':
            operators.append(ch)
        elif ch == ')':
            while operators[-1] != '(':
                apply_op(operators, values)
            operators.pop()
        i += 1
    while operators:
        apply_op(operators, values)
    return values[0]