def expression_to_postfix(expression):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def is_operator(char):
        return char in '+-*/^'

    def get_precedence(op):
        return prec[op] if op in prec else 0

    def apply_operation(op, stack, output):
        while stack and get_precedence(stack[-1]) >= get_precedence(op):
            output.append(stack.pop())
        stack.append(op)
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
        elif is_operator(expression[i]):
            tokens.append(expression[i])
            i += 1
        else:
            start = i
            while i < len(expression) and (not is_operator(expression[i])) and (not expression[i].isspace()):
                i += 1
            tokens.append(expression[start:i])
    stack = []
    output = []
    for token in tokens:
        if token.isdigit() or (len(token) > 1 and token[0] == '-' and token[1:].isdigit()):
            output.append(token)
        elif is_operator(token):
            apply_operation(token, stack, output)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            top_token = stack.pop()
            while top_token != '(':
                output.append(top_token)
                top_token = stack.pop()
    while stack:
        output.append(stack.pop())
    return ' '.join(output)