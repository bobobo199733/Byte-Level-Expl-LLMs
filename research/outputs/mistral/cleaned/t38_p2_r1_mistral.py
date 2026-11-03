def expression_to_postfix(expression):

    def apply_operator(op1, op2, operator):
        return {('+', float(op1), float(op2)): ' + ', ('-', float(op1), float(op2)): ' - ', ('*', float(op1), float(op2)): ' * ', ('/', float(op1), float(op2)): ' / '}[operator]

    def greater_precedence(op1, op2):
        return precedence[op1] > precedence[op2]
    operands = []
    operators_stack = []
    for token in expression.split():
        if token.isdigit() or token == '.':
            operands.append(token)
        elif token in operators:
            while operators_stack and operators_stack[-1] in operators and greater_precedence(operators[0], token):
                operands.append(operators_stack.pop())
            operators_stack.append(token)
        elif token == '(':
            operators_stack.append(token)
        elif token == ')':
            while operators_stack and operators_stack[-1] != '(':
                operands.append(operators_stack.pop())
            operators_stack.pop()
    while operators_stack:
        operands.append(operators_stack.pop())
    return ' '.join(operands) + ' '.join(reversed([apply_operator(*op) for op in zip(operators_stack, operands[-len(operators_stack):])]))