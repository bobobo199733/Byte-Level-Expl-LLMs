def is_operator(c):
    return c in ('+', '-', '*', '/')

def has_higher_precedence(op1, op2):
    prec = {'+': 1, '-': 1, '*': 3, '/': 3}
    return prec[op1] > prec[op2] or (prec[op1] == prec[op2] and op1 < op2)

def apply_operator(operand1, operand2, op):
    if op == '+':
        return operand1 + operand2
    elif op == '-':
        return operand1 - operand2
    elif op == '*':
        return operand1 * operand2
    else:
        return operand1 / operand2

def parse_number(s):
    i = 0
    for c in s:
        if not is_operator(c):
            yield from (c,)
            i += 1
        elif i > 0 and s[i - 1].isdigit():
            break

def parse_parentheses(s):
    depth = 0
    i = 0
    for c in s:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        if depth == 0:
            yield from (c,)
            i += 1
        if c == ')' and depth > 0:
            break

def parse(s):
    operators = set()
    operands = []
    i = 0
    for c in s:
        if not c or c.isspace():
            continue
        elif is_operator(c):
            operators.add(c)
        elif c == '(':
            subexp, _ = parse(s[i + 1:])
            operands.append((list(parse_parentheses(subexp)), ''))
            i += len(subexp) + 2
        else:
            operands.append((list(parse_number(s[i:])), c))
            i += len(str(next(iter(operands[-1][0])))) + 1
    if operators:
        for op, _ in sorted(operators.items(), key=lambda x: -x[1]):
            operands_to_combine = []
            for i, (operand, _) in enumerate(operands):
                if not operand or len(operand) < 2:
                    continue
                if op == '+' and operand[-1] == op:
                    operands_to_combine.append((operand, op))
                    break
                if op == '-' and has_higher_precedence(op, operand[0][-1]) or (op != '-' and (not operand[-1])):
                    operands_to_combine.append((operand, op))
            for combined_operand in operands_to_combine:
                operand, op = combined_operand
                operands[i - len(operand)] = (operand[0] + [apply_operator(*operand[-2], *operand[-1])], '')
                del operands[i:i + len(operand)]
    return next(iter(operands))[0][0] if operands else 0

def basic_calculator(s):
    return int(parse(s.replace(' ', '')))