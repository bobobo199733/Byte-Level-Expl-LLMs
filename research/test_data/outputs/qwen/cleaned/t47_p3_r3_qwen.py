def basic_calculator(s):

    def apply_operation(operators, values, operation):
        b = values.pop()
        a = values.pop()
        if operation == '+':
            values.append(a + b)
        elif operation == '-':
            values.append(a - b)
    operators = []
    values = []
    num = 0
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char in ['+', '-']:
            values.append(num)
            if operators and operators[-1] == '+':
                apply_operation(operators, values, '+')
            elif operators and operators[-1] == '-':
                apply_operation(operators, values, '-')
            operators.append(char)
            num = 0
        elif char == '(':
            operators.append('(')
        elif char == ')':
            if operators and operators[-1] != '(':
                apply_operation(operators, values, operators.pop())
            operators.pop()
    while operators:
        apply_operation(operators, values, operators.pop())
    return values[0]