def basic_calculator(s):
    """
    Evaluates a math string with +, -, *, /, (, ), and spaces.

    Args:
        s (str): A string containing a valid math expression.

    Returns:
        int: The integer result of the evaluated math expression.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    output = []
    tokens = s.replace(' ', '').split('+')
    for token in tokens:
        if token.strip() == '':
            continue
        for op in precedence.keys():
            if op in token:
                stack.append(token.split(op)[0])
                output.append((op, token.split(op)[1]))
                break
        else:
            stack.append(token)
    i = 0
    while '(' in stack and ')' in stack:
        open_bracket_idx = stack.index('(')
        close_bracket_idx = stack.index(')')
        while open_bracket_idx < close_bracket_idx and i <= close_bracket_idx:
            if stack[i] != '(' and stack[i] != ')':
                op, operand = output[i]
                pop1 = int(stack[open_bracket_idx])
                pop2 = int(operand)
                if op == '*':
                    result = pop1 * pop2
                elif op == '/':
                    result = pop1 // pop2
                stack.pop(open_bracket_idx)
                output.pop(i)
                output.insert(i, ('=', result))
                stack[open_bracket_idx] = str(result)
            i += 1
        stack.pop(close_bracket_idx)
        stack.pop(open_bracket_idx)
        output.pop(0)
        output.append(('=', stack[-1]))
    for op, operand in reversed(output):
        if op == '=':
            continue
        pop2 = int(operand)
        pop1 = int(stack.pop())
        if op == '*':
            result = pop1 * pop2
        elif op == '/':
            result = pop1 // pop2
        stack.append(str(result))
    return int(stack[-1])