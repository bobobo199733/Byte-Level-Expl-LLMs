def expression_to_postfix(expression):
    """
    Convert a mathematical infix expression into postfix notation.

    Args:
        expression (str): A string containing a mathematical infix expression.

    Returns:
        str: The equivalent postfix notation of the input expression.

    Example:
        >>> expression_to_postfix('A + B * C')
        'ABC*+'
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output_queue = []
    operators_stack = []
    for char in expression:
        if char == ' ':
            continue
        if char.isalnum():
            output_queue.append(char)
        elif char in precedence:
            while operators_stack and operators_stack[-1] in precedence and (precedence[operators_stack[-1]] >= precedence[char]):
                output_queue.append(operators_stack.pop())
            operators_stack.append(char)
        elif char == '(':
            operators_stack.append(char)
        elif char == ')':
            while operators_stack[-1] != '(':
                output_queue.append(operators_stack.pop())
            operators_stack.pop()
    while operators_stack:
        output_queue.append(operators_stack.pop())
    return ''.join(output_queue)