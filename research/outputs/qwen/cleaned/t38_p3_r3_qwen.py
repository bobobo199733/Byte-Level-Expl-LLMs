def precedence(op):
    if op in ('+', '-'):
        return 1
    elif op in ('*', '/'):
        return 2
    elif op == '^':
        return 3
    return 0

def expression_to_postfix(expression):
    output = []
    operators = []
    tokens = expression.replace(' ', '')
    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top_token = operators.pop()
            while top_token != '(':
                output.append(top_token)
                top_token = operators.pop()
        else:
            while operators and precedence(operators[-1]) >= precedence(token):
                output.append(operators.pop())
            operators.append(token)
    while operators:
        output.append(operators.pop())
    return ''.join(output)