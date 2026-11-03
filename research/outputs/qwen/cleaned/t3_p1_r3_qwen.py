def evaluate(expr: str) -> int:
    import re
    expr = expr.replace(' ', '')

    def calculate(op1, operator, op2):
        if operator == '+':
            return op1 + op2
        elif operator == '-':
            return op1 - op2
        elif operator == '*':
            return op1 * op2
        elif operator == '/':
            return int(op1 / op2)

    def shunting_yard(expr):
        operators = []
        operands = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        token_pattern = re.compile('(\\d+|[-+*/()])')
        for token in token_pattern.findall(expr):
            if token.isdigit():
                operands.append(int(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    op2 = operands.pop()
                    op1 = operands.pop()
                    operator = operators.pop()
                    operands.append(calculate(op1, operator, op2))
                if operators and operators[-1] == '(':
                    operators.pop()
            else:
                while operators and operators[-1] != '(' and (precedence[operators[-1]] >= precedence[token]):
                    op2 = operands.pop()
                    op1 = operands.pop()
                    operator = operators.pop()
                    operands.append(calculate(op1, operator, op2))
                operators.append(token)
        while operators:
            op2 = operands.pop()
            op1 = operands.pop()
            operator = operators.pop()
            operands.append(calculate(op1, operator, op2))
        return operands[0]
    try:
        result = shunting_yard(expr)
        return int(result)
    except (IndexError, ValueError):
        raise ValueError('Invalid expression')