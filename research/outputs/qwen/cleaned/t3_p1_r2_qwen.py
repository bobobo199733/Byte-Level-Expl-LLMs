def evaluate(expr: str) -> int:
    import re
    expr = expr.replace(' ', '')
    if not re.match('^[0-9+\\-*/()]*$', expr):
        raise ValueError('Invalid expression')

    def precedence(op: str) -> int:
        if op in '+-':
            return 1
        if op in '*/':
            return 2
        return 0

    def apply_operation(operands, operators):
        right = operands.pop()
        left = operands.pop()
        op = operators.pop()
        if op == '+':
            operands.append(left + right)
        elif op == '-':
            operands.append(left - right)
        elif op == '*':
            operands.append(left * right)
        elif op == '/':
            operands.append(int(left / right))

    def eval_expr(expr: str) -> int:
        stack = []
        num = ''
        operators = []
        for char in expr:
            if char.isdigit():
                num += char
            else:
                if num:
                    stack.append(int(num))
                    num = ''
                if char == '(':
                    stack.append(char)
                elif char == ')':
                    while stack and stack[-1] != '(':
                        apply_operation(stack, operators)
                    stack.pop()
                else:
                    while (stack and stack[-1] != '(') and precedence(operators) >= precedence(char):
                        apply_operation(stack, operators)
                    operators.append(char)
        if num:
            stack.append(int(num))
        while stack:
            apply_operation(stack, operators)
        return stack[0]
    return eval_expr(expr)