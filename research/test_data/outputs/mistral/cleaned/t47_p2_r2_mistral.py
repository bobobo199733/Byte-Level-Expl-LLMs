def basic_calculator(s):
    operators = {'+': lambda x, y: x + y, '-': lambda x, y: x - y}
    stack = []
    for token in s:
        if token.isdigit():
            stack.append(int(token))
        elif token == '(':
            sub_expr_stack = []
            stack.append((token, sub_expr_stack))
        elif token == ')':
            operator, sub_expr_stack = stack.pop()
            right = sub_expr_stack.pop()
            left = sub_expr_stack.pop()
            result = operators[operator](left, right)
            stack.append(result)
        elif token in operators:
            right = stack.pop()
            left = stack.pop()
            result = operators[token](left, right)
            stack.append(result)
    return stack[0]