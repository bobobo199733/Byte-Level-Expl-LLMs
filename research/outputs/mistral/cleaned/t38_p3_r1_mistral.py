def expression_to_postfix(expression):

    def apply_precedence(op1, op2):
        if precedence[op1] > precedence[op2]:
            return op1
        else:
            return op2
    stack = []
    output = []

    def process_token(token):
        if token.isalnum():
            output.append(token)
        elif token in operators:
            while stack and stack[-1] != '(' and (precedence[token] <= precedence[stack[-1]]):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
    for token in expression:
        process_token(token)
    while stack:
        output.append(stack.pop())
    return ' '.join(output)