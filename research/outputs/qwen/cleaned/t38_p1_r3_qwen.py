def expression_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def is_operator(char):
        return char in '+-*/^()'

    def to_token(value):
        if value.isalpha() or value.isdigit():
            return ('value', value)
        else:
            return ('operator', value)

    def higher_precedence(op1, op2):
        return precedence[op1] >= precedence[op2]

    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        values.append(f'({left} {operator} {right})')
    tokens = [to_token(char) for char in expression if not char.isspace()]
    operators_stack = []
    output_queue = []
    for token in tokens:
        if token[0] == 'value':
            output_queue.append(token[1])
        elif is_operator(token[1]):
            while operators_stack and higher_precedence(operators_stack[-1][1], token[1]) and (operators_stack[-1][1] != '('):
                apply_operator(operators_stack, output_queue)
            operators_stack.append(token)
        elif token[1] == '(':
            operators_stack.append(token)
        elif token[1] == ')':
            while operators_stack and operators_stack[-1][1] != '(':
                apply_operator(operators_stack, output_queue)
            if operators_stack and operators_stack[-1][1] == '(':
                operators_stack.pop()
    while operators_stack:
        apply_operator(operators_stack, output_queue)
    return ' '.join(output_queue)