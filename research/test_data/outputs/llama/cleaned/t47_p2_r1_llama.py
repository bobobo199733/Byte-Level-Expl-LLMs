def basic_calculator(s):
    """
    Evaluates a string math expression and returns the result.
    
    The string must contain non-negative integers, operators + or -, 
    parentheses ( and ), and spaces (which are ignored).
    
    :param s: String representing the math expression.
    :return: Integer result of the evaluation.
    """
    stack = []
    num = 0
    sign = '+'
    for i in range(len(s)):
        if s[i] == ' ':
            continue
        if s[i].isdigit():
            num = num * 10 + int(s[i])
        elif s[i] in '+-':
            stack.append(num)
            num = 0
            sign = s[i]
            while s[i] == ')' and i < len(s) - 1:
                close_i = i + 1
                open_i = close_i
                depth = 1
                while depth > 0 and close_i < len(s):
                    if s[close_i] == '(':
                        depth += 1
                    elif s[close_i] == ')':
                        depth -= 1
                    close_i += 1
                expr_inside_parentheses = s[open_i:close_i - 1]
                num = basic_calculator(expr_inside_parentheses)
                stack.append(num)
                sign = '+'
                i = close_i - 1
        elif s[i] == '(':
            i += 2 if i + 1 < len(s) else 0
            continue
        elif s[i] == ')':
            stack.append(num)
            num = 0
    if sign == '+':
        return sum(stack)
    elif sign == '-':
        return -sum(stack) + basic_calculator(s[num + 1:])