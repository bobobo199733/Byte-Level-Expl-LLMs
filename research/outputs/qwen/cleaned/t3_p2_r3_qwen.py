def evaluate(expr: str) -> int:

    def apply_op(op, reg1, reg2):
        if op == '+':
            return reg1 + reg2
        elif op == '-':
            return reg1 - reg2
        elif op == '*':
            return reg1 * reg2
        elif op == '/':
            return int(reg1 / reg2)

    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def operate(stack, ops_stack):
        op = ops_stack.pop()
        right = stack.pop()
        left = stack.pop()
        result = apply_op(op, left, right)
        stack.append(result)
    expr = expr.replace(' ', '')
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isdigit():
            start = i
            while i + 1 < len(expr) and expr[i + 1].isdigit():
                i += 1
            tokens.append(int(expr[start:i + 1]))
            i -= 1
        elif expr[i] in ('+', '-', '*', '/'):
            if expr[i] == '(':
                count = 0
                for j in range(i + 1, len(expr)):
                    if expr[j] == '(':
                        count += 1
                    if expr[j] == ')':
                        count -= 1
                    if count == 0:
                        break
                tokens.append(evaluate(expr[i + 1:j]))
            else:
                while ops_stack and precedence(ops_stack[-1]) >= precedence(expr[i]):
                    operate(stack, ops_stack)
                ops_stack.append(expr[i])
        i += 1
    for op in reversed(ops_stack):
        operate(stack, [op])
    return stack[0]