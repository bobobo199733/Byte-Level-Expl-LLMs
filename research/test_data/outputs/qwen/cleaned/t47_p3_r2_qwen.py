def basic_calculator(s: str) -> int:

    def apply_op(op, b, a):
        return a + b if op == '+' else a - b

    def compute(expression):
        operand = 0
        stack = []
        sign = 1
        result = 0
        for char in expression:
            if char.isdigit():
                operand = operand * 10 + int(char)
            elif char == '+':
                result += sign * operand
                operand = 0
                sign = 1
            elif char == '-':
                result += sign * operand
                operand = 0
                sign = -1
            elif char == '(':
                stack.append(result)
                stack.append(sign)
                sign, result = (1, 0)
            elif char == ')':
                result += sign * operand
                result *= stack.pop()
                result += stack.pop()
                operand = 0
        if operand:
            result += sign * operand
        return result
    s = s.replace(' ', '')
    return compute(s)