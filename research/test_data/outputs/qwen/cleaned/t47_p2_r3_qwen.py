def basic_calculator(s):

    def pop_and_apply_operator(stack, operator):
        right = stack.pop()
        left = stack.pop()
        if operator == '+':
            stack.append(left + right)
        elif operator == '-':
            stack.append(left - right)
    s = s.replace(' ', '')
    stack = [0]
    current_number = 0
    current_sign = 1
    result = 0
    for char in s:
        if char.isdigit():
            current_number = current_number * 10 + int(char)
        elif char == '+':
            result += current_sign * current_number
            current_sign = 1
            current_number = 0
        elif char == '-':
            result += current_sign * current_number
            current_sign = -1
            current_number = 0
        elif char == '(':
            stack.append(result)
            stack.append(current_sign)
            result = 0
            current_sign = 1
        elif char == ')':
            result += current_sign * current_number
            current_number = 0
            prev_result = stack.pop()
            prev_sign = stack.pop()
            result *= prev_sign
            result += prev_result
    result += current_sign * current_number
    return result