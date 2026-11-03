def basic_calculator(s):
    """
    Evaluates a math string with +, -, parentheses, and spaces.

    Args:
        s (str): Math string to evaluate.

    Returns:
        int: Result of the evaluation.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    tokens = s.replace(' ', '').split('(')
    tokens = [token.replace(')', '') for token in tokens]
    output_queue = []
    operator_stack = []
    for token in tokens:
        if token == '':
            continue
        try:
            num = int(token)
            output_queue.append(num)
        except ValueError:
            while operator_stack and precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0):
                output_queue.append(operator_stack.pop())
            if token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
            else:
                operator_stack.append(token)
    while operator_stack:
        output_queue.append(operator_stack.pop())
    stack = []
    for token in output_queue:
        if isinstance(token, int):
            stack.append(token)
        elif token == '+':
            num2 = stack.pop()
            num1 = stack.pop()
            stack.append(num1 + num2)
        elif token == '-':
            num2 = stack.pop()
            num1 = stack.pop()
            stack.append(num1 - num2)
    return stack[0]