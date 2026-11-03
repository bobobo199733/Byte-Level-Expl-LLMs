import operator as op

def evaluate(expr: str) -> int:
    expr = expr.replace(' ', '')
    ops = {'+': op.add, '-': op.sub, '*': op.mul, '/': lambda a, b: a // b}
    stack = []
    op_stack = []
    for char in expr:
        if char.isdigit():
            stack.append(int(char))
        elif char in ops:
            while len(op_stack) > 0 and op_stack[-1] != '(' and (get_precedence(op_stack[-1]) >= get_precedence(char)):
                apply_op(stack, op_stack.pop(), ops)
            op_stack.append(char)
        elif char == '(':
            op_stack.append(char)
        elif char == ')':
            while len(op_stack) > 0 and op_stack[-1] != '(':
                apply_op(stack, op_stack.pop(), ops)
            if op_stack[-1] == '(':
                op_stack.pop()
    while len(op_stack) > 0:
        apply_op(stack, op_stack.pop(), ops)
    if len(stack) != 1:
        raise ValueError('Invalid expression')
    return stack[0]

def get_precedence(char):
    """Returns the precedence of an operator"""
    return {'+': 1, '-': 1, '*': 2, '/': 2}.get(char)

def apply_op(stack, op, ops):
    """Applies an operation with two operands on top of the stack"""
    b = stack.pop()
    a = stack.pop()
    if op == '(':
        stack.append(a)
        stack.append(b)
    else:
        result = ops[op](a, b)
        stack.append(result)