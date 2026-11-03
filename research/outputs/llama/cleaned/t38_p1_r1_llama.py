def expression_to_postfix(expression):
    """
    Converts an infix expression into its equivalent postfix notation.

    :param expression: Infix mathematical expression as a string.
    :return: Postfix notation of the input expression as a list of tokens (operators and operands).
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output_queue = []
    operator_stack = []
    for token in expression.split():
        if token not in precedence:
            output_queue.append(token)
        else:
            while operator_stack and precedence[token] <= precedence[operator_stack[-1]]:
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
    while operator_stack:
        output_queue.append(operator_stack.pop())
    return output_queue