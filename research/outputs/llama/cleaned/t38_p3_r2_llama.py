def expression_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    if not expression.strip():
        return ''
    tokens = []
    current_token = ''
    for char in expression:
        if char.isspace():
            continue
        elif char == '(':
            if current_token and current_token != '-':
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        elif char == ')':
            if current_token and current_token != '-':
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        else:
            current_token += char
            if char in precedence or char == '+' or char == '-' or (char == '*') or (char == '/'):
                if current_token and current_token != '-':
                    tokens.append(current_token)
                    current_token = ''
                tokens.append(char)
    if current_token:
        tokens.append(current_token)
    output = []
    stack = []
    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and (precedence.get(token, 0) <= precedence.get(stack[-1], 0)):
                output.append(stack.pop())
            stack.append(token)
    while stack:
        if stack[-1] == '(':
            raise ValueError('Unbalanced parentheses')
        output.append(stack.pop())
    return ' '.join(output)