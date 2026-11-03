def basic_calculator(s: str) -> int:
    """
    Evaluates a string math expression containing non-negative integers, +, -, (, ) and spaces.
    
    Args:
        s (str): The input math expression as a string.
    
    Returns:
        int: The result of the evaluated expression.
    """
    stack = []
    sign = 1
    num = 0
    for c in s:
        if c == ' ':
            continue
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == '+':
            stack.append(sign * num)
            sign = 1
            num = 0
        elif c == '-':
            stack.append(sign * num)
            sign = -1
            num = 0
        elif c == '(':
            stack.append(num)
            num = 0
        elif c == ')':
            stack.append(sign * num)
            num = 0
            total = 0
            while stack and stack[-1] != '+':
                total += stack.pop()
            if stack:
                stack[-1] += total
            else:
                stack.append(total)
    total = 0
    while stack:
        total += stack.pop()
    return total