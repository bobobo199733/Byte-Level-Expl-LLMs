def expression_to_postfix(expression):

    def apply_operators(operators, stack):
        i = len(operators) - 1
        while i >= 0:
            operator = operators[i]
            if not operator or operator == '(':
                i -= 1
                continue
            precedence2 = precedence[operator] if operator else 0
            while stack and (precedence[stack[-1]] > precedence2 or stack[-1] == '('):
                postfix.append(stack.pop())
            operators[i] = None
            i -= 1
        return
    infix = expression.replace(' ', '')
    operators = []
    operands = []
    postfix = []
    for token in infix:
        if token.isalpha():
            postfix.append(token)
        elif token in '()':
            operators.append(token)
        elif token in ['+', '-', '*', '/']:
            apply_operators(operators, stack=operands)
            operators.append(token)
    apply_operators(operators, operands)
    while operators:
        postfix.append(operators.pop())
    return ' '.join(postfix)