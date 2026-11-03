def expression_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def apply_operator(operators, values):
        right = values.pop()
        left = values.pop()
        operators.append(f'({left} {right})')
    tokens = expression.replace(' ', '')
    token_list = []
    for char in tokens:
        if char.isalnum():
            token_list.append(char)
        else:
            token_list.append(' ' + char + ' ')
    operators_stack = []
    output_queue = []
    for token in token_list:
        if token.isalnum():
            output_queue.append(token)
        elif token == '(':
            operators_stack.append('(')
        elif token == ')':
            while operators_stack and operators_stack[-1] != '(':
                apply_operator(operators_stack, output_queue)
            operators_stack.pop()
        else:
            while operators_stack and operators_stack[-1] != '(' and (precedence[operators_stack[-1]] >= precedence[token]):
                apply_operator(operators_stack, output_queue)
            operators_stack.append(token)
    while operators_stack:
        if operators_stack[-1] == '(':
            raise ValueError('Unmatched parenthesis in input expression')
        apply_operator(operators_stack, output_queue)
    return ''.join(output_queue)