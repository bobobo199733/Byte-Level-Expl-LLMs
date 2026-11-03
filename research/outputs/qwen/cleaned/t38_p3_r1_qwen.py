def expression_to_postfix(expression):

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
            values.append(left / right)

    def greater_precedence(op1, op2):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        return precedence[op1] > precedence[op2]
    operators = []
    values = []
    tokens = expression.split()
    for token in tokens:
        if token.isdigit():
            values.append(int(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while len(operators) != 0 and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()
        else:
            while len(operators) != 0 and greater_precedence(operators[-1], token):
                apply_operator(operators, values)
            operators.append(token)
    while len(operators) != 0:
        apply_operator(operators, values)
    return ' '.join(map(str, values))