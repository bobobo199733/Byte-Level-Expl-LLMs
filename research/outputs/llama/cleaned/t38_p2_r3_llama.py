def expression_to_postfix(expression):
    """
    Converts an infix mathematical expression into postfix notation.

    Args:
        expression (str): A string representing the infix mathematical expression.

    Returns:
        str: The equivalent postfix notation of the input expression.

    Example:
        >>> expression_to_postfix("A+B*C")
        'ABC*+'
        >>> expression_to_postfix("(A+B)*C")
        'AB+C*'
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []
    expression = expression.replace(' ', '')
    for char in expression:
        if char.isalpha():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] in precedence and (precedence[stack[-1]] >= precedence[char]):
                output.append(stack.pop())
            stack.append(char)
    while stack:
        if stack[-1] == '(':
            raise ValueError('Unbalanced parentheses')
        output.append(stack.pop())
    return ''.join(output)