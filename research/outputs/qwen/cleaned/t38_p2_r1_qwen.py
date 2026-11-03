def expression_to_postfix(expression):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}
    stack = []
    output = []
    for char in expression.replace(' ', ''):
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            top_token = stack.pop()
            while top_token != '(':
                output.append(top_token)
                top_token = stack.pop()
        else:
            while stack and prec[stack[-1]] >= prec[char]:
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return ''.join(output)