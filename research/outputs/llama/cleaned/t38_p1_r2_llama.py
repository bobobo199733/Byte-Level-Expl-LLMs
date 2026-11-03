def expression_to_postfix(expression):
    """
    Converts an infix expression into postfix notation.

    :param expression: The infix expression as a string
    :return: The postfix expression as a string
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output_queue = []
    operator_stack = []
    for char in expression:
        if char.isalnum():
            output_queue.append(char)
        elif char == ')':
            operator_stack.append(char)
        elif char == '(':
            while True:
                top = operator_stack.pop()
                if top == '(':
                    break
                output_queue.append(top)
            operator_stack.pop()
        else:
            while operator_stack and operator_stack[-1] != ')' and (precedence[char] <= precedence[operator_stack[-1]]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(char)
    while operator_stack:
        top = operator_stack.pop()
        if top == ')':
            raise ValueError('Unbalanced parentheses')
        output_queue.append(top)
    return ''.join(output_queue)