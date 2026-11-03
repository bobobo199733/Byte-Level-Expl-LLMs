def expression_to_postfix(expression):
    prec = {'(': 0, '+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    output = []
    tokens = iter(expression.replace(' ', ''))

    def get_next_token():
        try:
            return next(tokens)
        except StopIteration:
            return None
    while True:
        token = get_next_token()
        if token is None:
            break
        elif token == '(':
            stack.append(token)
        elif token in '0123456789':
            output.append(token)
            while True:
                next_token = get_next_token()
                if next_token and next_token.isdigit():
                    output.append(next_token)
                else:
                    tokens.seek(-1, 1)
                    break
        elif token in '+-*/^':
            while stack and prec[stack[-1]] >= prec[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == ')':
            top_token = stack.pop()
            while top_token != '(':
                output.append(top_token)
                top_token = stack.pop()
    while stack:
        output.append(stack.pop())
    return ''.join(output)