def basic_calculator(s):
    """
    Evaluates a mathematical expression given as a string.

    Args:
        s (str): The mathematical expression to evaluate.

    Returns:
        int: The result of the evaluation as an integer.
    """
    s = s.replace(' ', '')
    precedence = {'+': 1, '-': 1}
    stack = []
    curr_operand = ''
    for char in s:
        if char.isdigit() or char == '(':
            curr_operand += char
        elif char == ')':
            while stack[-1] != '(':
                stack.append(stack.pop())
            stack.pop()
            stack.append(int(curr_operand))
            curr_operand = ''
        elif char in precedence:
            while stack and stack[-1] != '' and (precedence[stack[-1]] >= precedence[char]):
                operand = int(stack.pop())
                op = stack.pop()
                if op == '+':
                    stack.append(operand + curr_operand)
                elif op == '-':
                    stack.append(-operand + curr_operand)
                else:
                    raise ValueError('Invalid operator')
            stack.append(char)
            curr_operand = ''
    while stack and stack[-1] != '':
        operand = int(stack.pop())
        op = stack.pop()
        if op == '+':
            stack.append(operand + int(curr_operand))
        elif op == '-':
            stack.append(-operand + int(curr_operand))
        else:
            raise ValueError('Invalid operator')
    return stack[0]