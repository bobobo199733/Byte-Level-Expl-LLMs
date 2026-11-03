def expression_to_postfix(expression):
    """
    Convert a mathematical infix expression into postfix notation.

    Args:
        expression (str): Infix expression as string, ignoring whitespace.

    Returns:
        str: Postfix expression as string.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    postfix = ''
    operator_stack = []
    tokens = []
    token = ''
    for char in expression:
        if char.isspace():
            continue
        elif char == '(' or char == ')':
            tokens.append(token + char)
            token = ''
        else:
            token += char
            if char == '+' or char == '-' or char == '*' or (char == '/'):
                tokens.append(token)
                token = ''
    tokens.append(token)
    for token in tokens:
        if token in precedence:
            while operator_stack and precedence[operator_stack[-1]] >= precedence[token]:
                postfix += operator_stack.pop() + ' '
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                postfix += operator_stack.pop() + ' '
            if len(operator_stack) > 0:
                operator_stack.pop()
        else:
            postfix += token + ' '
    while operator_stack:
        postfix += operator_stack.pop() + ' '
    return postfix.strip()