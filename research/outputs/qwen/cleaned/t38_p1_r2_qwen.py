def expression_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def is_operator(char):
        return char in '+-*/^()'

    def higher_precedence(op1, op2):
        return precedence[op1] >= precedence[op2]
    output = []
    operators = []
    for char in expression:
        if char.isalpha():
            output.append(char)
        elif char == '(':
            operators.append(char)
        elif char == ')':
            top = operators.pop()
            while top != '(':
                output.append(top)
                top = operators.pop()
        else:
            while operators and operators[-1] != '(' and higher_precedence(operators[-1], char):
                output.append(operators.pop())
            operators.append(char)
    while operators:
        output.append(operators.pop())
    return ''.join(output)