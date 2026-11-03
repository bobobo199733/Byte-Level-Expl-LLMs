def basic_calculator(s: str) -> int:

    def apply_operator(operators, values):
        right = values.pop()
        left = values.pop()
        operator = operators.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)

    def greater_precedence(op1, op2):
        precedence = {'+': 1, '-': 1}
        return precedence[op1] >= precedence[op2]
    operators = []
    values = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        if s[i].isdigit():
            value = 0
            while i < len(s) and s[i].isdigit():
                value = value * 10 + int(s[i])
                i += 1
            values.append(value)
        elif s[i] in '+-':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.append(s[i])
        elif s[i] == '(':
            operators.append(s[i])
        elif s[i] == ')':
            while operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()
            i += 1
        else:
            raise ValueError(f'Invalid character: {s[i]}')
        i += 1
    while operators:
        apply_operator(operators, values)
    return values[0]