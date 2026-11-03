import operator

def evaluate(expr: str) -> int:
    """
    Evaluate an arithmetic expression and return the integer result.

    Args:
        expr (str): The arithmetic expression to evaluate, e.g., "1 + 2 * 3"

    Returns:
        int: The integer result of the evaluated expression.

    Raises:
        ValueError: If the expression is invalid.
    """
    precedence = {operator.add: 1, operator.sub: 1, operator.mul: 2, operator.truediv: 3}
    tokens = expr.replace(' ', '').split()
    op_stack = []
    num_stack = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.isdigit():
            num_stack.append(int(token))
        elif token in precedence:
            while op_stack and (token in precedence and precedence[precedence[op_stack[-1]]] >= precedence[token]):
                num2 = num_stack.pop()
                num1 = num_stack.pop()
                op = op_stack.pop()
                if op == operator.truediv:
                    result = operator.floordiv(num1, num2)
                else:
                    result = op(num1, num2)
                num_stack.append(result)
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack[-1] != '(':
                num2 = num_stack.pop()
                num1 = num_stack.pop()
                op = op_stack.pop()
                if op == operator.truediv:
                    result = operator.floordiv(num1, num2)
                else:
                    result = op(num1, num2)
                num_stack.append(result)
            op_stack.pop()
        i += 1
    while op_stack:
        num2 = num_stack.pop()
        num1 = num_stack.pop()
        op = op_stack.pop()
        if op == operator.truediv:
            result = operator.floordiv(num1, num2)
        else:
            result = op(num1, num2)
        num_stack.append(result)
    return num_stack[0]