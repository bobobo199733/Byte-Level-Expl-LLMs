precedence = {'^': 3, '*', '/': 2, '+', '-': 1, '(': 0}

operators = {
    '+': ['-', '*', '/'],
    '-': ['-', '*', '/'],
    '*': ['/'],
    '/': ['*', '/']
}

def expression_to_postfix(expression):
    stack, output = [], []

    for token in expression:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            top_token = stack.pop()
            while top_token != '(':
                output.append(stack.pop())
                if top_token:
                    top_token = stack.pop()
        else:
            while (stack and stack[-1] != '(' and
                   precedence[token] <= precedence[stack[-1]]):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return ' '.join(output)