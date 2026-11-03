def expression_to_postfix(expression):
    """
    Converts an infix expression to postfix notation.

    Args:
        expression (str): Infix expression as a string.

    Returns:
        str: Postfix equivalent of the input expression.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    operator_stack = []
    postfix = []
    for char in expression:
        if char.isalnum():
            postfix.append(char)
        elif char == '(':
            operator_stack.append(char)
        elif char == ')':
            while True:
                top = operator_stack.pop()
                if top == '(':
                    break
                postfix.append(top)
            postfix.append(char)
        elif char in precedence:
            while operator_stack and operator_stack[-1] != '(' and (precedence[operator_stack[-1]] >= precedence[char]):
                postfix.append(operator_stack.pop())
            operator_stack.append(char)
    while operator_stack:
        top = operator_stack.pop()
        if top == '(':
            raise ValueError('Unbalanced parentheses')
        postfix.append(top)
    return ' '.join(postfix)