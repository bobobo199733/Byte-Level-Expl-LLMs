def basic_calculator(expression):

    def apply_operation(operators, numbers):
        while operators:
            op = operators.pop()
            num1 = numbers.pop()
            num2 = numbers.pop()
            if op == '+':
                numbers.append(num2 + num1)
            elif op == '-':
                numbers.append(num2 - num1)

    def parse_expression():
        current_number = ''
        operands = []
        operators = []
        for char in expression:
            if char.isdigit():
                current_number += char
            elif char == '(':
                operands.append(int(current_number))
                current_number = ''
                operators.append((char, []))
            elif char == ')':
                apply_operation(operators[-1][1], operands)
                operators[-1] = ('', operators[-1][1])
                operator = operators.pop()
                operands.append(operator[0])
                while operator[1]:
                    operator = operator[1].pop()
                    operands.append(int(current_number))
                    current_number = ''
                    apply_operation((operator, []), operands)
            elif char in '+-':
                if current_number:
                    operands.append(int(current_number))
                    current_number = ''
                operators[-1][1].append((char, []))
            else:
                raise ValueError(f"Unknown operator '{char}'")
        if current_number:
            operands.append(int(current_number))
        apply_operation(operators[-1][1], operands)
    try:
        parse_expression()
        return operands[0]
    except ValueError as e:
        raise ValueError('Invalid expression') from e