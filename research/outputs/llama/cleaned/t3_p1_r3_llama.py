def evaluate(expr: str) -> int:
    """
    Evaluates an arithmetic expression and returns the integer result.

    Args:
        expr (str): The expression to evaluate, ignoring whitespace.

    Returns:
        int: The integer result of the evaluated expression.

    Raises:
        ValueError: If the expression is invalid.
    """
    operators = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: int(x / y) if isinstance(x, int) and isinstance(y, int) else x / y}
    stack = []
    curr_expr = ''
    i = 0
    while i < len(expr):
        char = expr[i]
        if char.isdigit() or char == '.':
            curr_expr += char
        elif char in operators:
            if not stack:
                raise ValueError('Invalid expression: missing operand')
            num = int(curr_expr) if curr_expr else stack.pop()
            func = operators[char]
            if expr[i + 1] == '(':
                i += 2
                arg = evaluate(expr[i:])
                i = len(expr)
                num = func(num, arg)
            else:
                op = stack.pop()
                if isinstance(op, str):
                    raise ValueError('Invalid expression: unsupported operator')
                num = func(op, num)
            stack.append(num)
            curr_expr = ''
        elif char == '(':
            stack.append(char)
        elif char == ')':
            if not stack or stack[-1] != '(':
                raise ValueError('Invalid expression: mismatched parentheses')
            while stack and isinstance(stack[-1], int) or (isinstance(stack[-1], str) and stack[-1] in operators):
                num = stack.pop()
                if isinstance(num, str):
                    func = operators[num]
                else:
                    func = lambda x, y: x + y
                op = stack.pop() if stack else 0
                num = func(op, num)
                stack.append(num)
        else:
            raise ValueError(f"Invalid expression: unexpected character '{char}'")
        i += 1
    while stack and isinstance(stack[-1], int) or (isinstance(stack[-1], str) and stack[-1] in operators):
        num = stack.pop()
        if isinstance(num, str):
            func = operators[num]
        else:
            func = lambda x, y: x + y
        op = stack.pop() if stack else 0
        num = func(op, num)
        stack.append(num)
    if stack and isinstance(stack[-1], int):
        raise ValueError('Invalid expression: unexpected trailing digits')
    return stack[0]