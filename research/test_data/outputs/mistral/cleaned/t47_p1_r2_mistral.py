import re

def basic_calculator(expression):

    def parse_parentheses(expr):
        return '('.join([parse_parentheses(inner) for inner in re.findall('\\(([\\w\\s]+)\\)', expr)]) if expr else ''

    def calculate(operators, numbers):
        total = 0
        current_number = 0
        for operator, number in zip(operators, numbers):
            if operator == '-':
                current_number -= number
            else:
                current_number += number
            total += current_number
            current_number = 0
        return total + current_number
    operators = re.findall('[+-]', expression)
    numbers = [int(number.strip()) for number in re.split('[+-()]', expression) if number.strip()]
    numbers[numbers.index('+')] = calculate(parse_parentheses(numbers[numbers.index('('):numbers.index(')') + 1]), numbers[numbers[numbers.index('('):].index('+') + 1:])
    numbers[numbers.index('-')] = calculate(parse_parentheses(numbers[numbers.index('('):numbers.index(')') + 1]), numbers[numbers[numbers.index('('):].index('-') + 1:])
    return calculate(operators, numbers)