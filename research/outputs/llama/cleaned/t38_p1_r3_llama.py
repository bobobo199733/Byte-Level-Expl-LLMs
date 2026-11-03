def expression_to_postfix(expression):
    """
    Converts an infix expression into postfix notation.

    Args:
        expression (str): The infix expression to be converted.

    Returns:
        str: The equivalent postfix expression.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []
    for char in expression:
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1].isalnum() == False and (precedence[stack[-1]] >= precedence[char]):
                output.append(stack.pop())
            stack.append(char)
    while stack:
        if stack[-1] != '(':
            output.append(stack.pop())
        else:
            break
    return ''.join(output)