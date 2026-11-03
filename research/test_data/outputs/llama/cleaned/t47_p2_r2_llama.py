def basic_calculator(s):
    """
    Evaluates a string math expression containing non-negative integers, 
    operators + and -, parentheses ( and ), and spaces.

    Args:
        s (str): The input string expression

    Returns:
        int: The result of the evaluated expression
    """
    tokens = s.split()
    stack = []
    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            value, operator = pop_and_get_operator(stack)
            intermediate_result, _ = evaluate_expression(value, operator, stack)
            stack.pop()
            stack.append(intermediate_result)
        elif token == '+':
            stack.append(token)
        elif token == '-':
            value, prev_operator = pop_and_get_operator(stack)
            intermediate_result = evaluate_expression(value, prev_operator, stack)
            stack.pop()
            stack.append(intermediate_result)
        else:
            value = int(token)
            stack.append(value)
    final_value, _ = pop_and_get_operator(stack)
    return final_value

def pop_and_get_operator(stack):
    """
    Pops a value and operator from the top of the stack.

    Args:
        stack (list): The input stack

    Returns:
        tuple: A pair containing the popped value and operator
    """
    value = stack.pop()
    operator = stack.pop()
    return (value, operator)

def evaluate_expression(value, operator, stack):
    """
    Evaluates an expression by popping numbers and operators from the stack.

    Args:
        value (int): The current intermediate result
        operator (str): The operator (+ or -)
        stack (list): The input stack

    Returns:
        tuple: A pair containing the final result and the next operator
    """
    while True:
        if stack[-1] == '+':
            value += stack.pop()
        elif stack[-1] == '-':
            value -= stack.pop()
        else:
            break
    return (value, operator)