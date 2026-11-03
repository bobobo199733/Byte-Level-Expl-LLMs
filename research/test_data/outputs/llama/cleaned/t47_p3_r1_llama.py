def basic_calculator(s):
    """
    Evaluates a math string with +, -, (, ), and spaces.

    Args:
        s (str): The math string to evaluate.

    Returns:
        int: The integer result of the calculation.
    """
    num_stack = []
    op_stack = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        if s[i].isdigit() or s[i] == '.':
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            num_stack.append(float(s[i:j]))
            i = j
        elif s[i] in '+-*/':
            while op_stack and op_stack[-1] != '(' and (get_precedence(op_stack[-1]) >= get_precedence(s[i])):
                apply_op(num_stack, op_stack)
            op_stack.append(s[i])
            i += 1
        elif s[i] == '(':
            op_stack.append('(')
            i += 1
        elif s[i] == ')':
            while op_stack[-1] != '(':
                apply_op(num_stack, op_stack)
            op_stack.pop()
            i += 1
    while op_stack:
        apply_op(num_stack, op_stack)
    return int(num_stack[0])