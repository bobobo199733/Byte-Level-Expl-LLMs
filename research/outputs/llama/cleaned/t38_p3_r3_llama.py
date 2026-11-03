def expression_to_postfix(expression):
    """
    Convert an infix expression into postfix notation.

    Args:
        expression (str): The infix expression as a string.

    Returns:
        str: The equivalent postfix expression.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operator_stack = []
    for char in expression:
        if char.isspace():
            continue
        elif char in ['(', ')']:
            if char == '(':
                operator_stack.append(char)
            else:
                while operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                operator_stack.pop()
        elif char in precedence:
            while operator_stack and operator_stack[-1] != '(' and (precedence[operator_stack[-1]] >= precedence[char]):
                output.append(operator_stack.pop())
            operator_stack.append(char)
        else:
            output.append(char)
    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError('Unbalanced parentheses in the input expression')
        output.append(operator_stack.pop())
    return ''.join(output)