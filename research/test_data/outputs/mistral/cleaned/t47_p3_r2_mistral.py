def basic_calculator(expression):

    def process_number(numbers):
        result = 0
        for number in numbers:
            result += int(number)
        return result
    current_numbers = []
    operators = {'+': 1, '-': 1}
    for char in expression:
        if char.isdigit():
            current_numbers.append(char)
        elif char in operators:
            if current_numbers:
                result = process_number(current_numbers)
                current_numbers = []
                if char == '-':
                    result *= -1
                current_numbers.append(result)
                current_numbers.append(char)
        elif char == ' ':
            continue
        else:
            raise ValueError('Invalid character found in the expression.')
    result = process_number(current_numbers)
    return result