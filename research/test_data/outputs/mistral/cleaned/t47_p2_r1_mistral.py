def basic_calculator(s):

    def apply_operators(stack):
        while len(stack) > 1 and stack[-2] not in ['(', '+', '-']:
            right = stack.pop()
            left = stack.pop()
            operator = stack.pop()
            if operator == '+':
                stack.append(left + right)
            elif operator == '-':
                stack.append(left - right)

    def handle_parentheses(s, stack):
        parentheses_stack = []
        for char in s:
            if char == '(':
                parentheses_stack.append(char)
            elif char == ')':
                while parentheses_stack and parentheses_stack[-1] != '(':
                    parentheses_stack.pop()
                    apply_operators(stack)
                parentheses_stack.pop()
    stack = []
    for char in s:
        if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            number = ''
            while len(s) > 0 and s[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                number += s.pop()
            stack.append(int(number))
        elif char in ['+', '-']:
            apply_operators(stack)
            stack.append(char)
        elif char == '(':
            handle_parentheses(s, stack)
    if len(stack) > 1:
        raise ValueError('Invalid expression')
    result = stack[0]
    return result