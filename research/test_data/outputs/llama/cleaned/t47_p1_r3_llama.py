def basic_calculator(s):
    """
    Evaluates a mathematical expression given as a string and returns the result as an integer.

    Args:
        s (str): The mathematical expression to evaluate.

    Returns:
        int: The result of the evaluated expression.
    """
    stack = []
    curr_num = 0
    res = 0
    sign = 1
    for i, c in enumerate(s):
        if not c.isdigit():
            if c == '+':
                res += curr_num * sign
            elif c == '-':
                res += curr_num * sign
                sign = -1
            else:
                stack.append(curr_num)
                stack.append(sign)
                curr_num = 0
                sign = 1
            continue
        curr_num = curr_num * 10 + int(c)
    res += curr_num * sign
    while len(stack) > 1:
        num2 = stack.pop()
        num1 = stack.pop()
        op = stack.pop()
        if op == '+':
            stack.append(num1 + num2)
        elif op == '-':
            stack.append(num1 - num2)
    return res + stack[0]