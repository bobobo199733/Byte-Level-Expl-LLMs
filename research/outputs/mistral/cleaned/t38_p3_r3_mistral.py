def precedence(op):
    if op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/':
        return 2
    else:
        return 0

def associate_with_left(s):
    return s + ')'

def expression_to_postfix(expression):

    def is_operator(ch):
        return ch in ['+', '-', '*', '/']

    def pop_and_append(stack, op):
        while len(stack) > 0 and precedence(op) <= precedence(stack[-1]):
            postfix.append(stack.pop())
        stack.append(op)
    operators = set('+-*/')
    operands = []
    postfix = []
    parentheses = set('([{')
    for char in expression:
        if char in operators:
            pop_and_append(stack, char)
        elif char in parentheses:
            if char == '(':
                stack.append(char)
            elif char == ')':
                top = stack.pop()
                while top != '(':
                    postfix.append(top)
                    top = stack.pop()
        elif char in set('0123456789.'):
            operands.append(char)
    while len(stack) > 0:
        postfix.append(stack.pop())
    for opnd in reversed(operands):
        postfix.append(opnd)
    return ' '.join(postfix)