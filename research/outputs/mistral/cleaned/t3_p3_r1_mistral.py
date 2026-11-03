def precedence(operators):
    return {'+': 1, '-': 1, '*': 2, '/': 2}[operators]

def associate_right(operators):
    return operators != '+' and operators != '-'

def evaluate(expr: str) -> int:

    def _evaluate(tokens, pos=0):
        while pos < len(tokens):
            token = tokens[pos]
            if token.isdigit():
                result = int(token)
                pos += 1
                return result
            elif token == '(':
                pos += 1
                subresult = _evaluate(tokens, pos)
                operators = tokens[pos]
                pos += 1
                right_subresult = _evaluate(tokens, pos)
                if operators != ')' or subresult is None or right_subresult is None:
                    raise ValueError('Invalid expression')
                if operators == '/':
                    result = int(subresult / right_subresult // 1)
                else:
                    result = subresult if operators == '+' else subresult - right_subresult
            else:
                next_pos = min([i for i in range(pos + 1, len(tokens)) if tokens[i] != '(' or tokens[i] == ')'])
                left_operators = tokens[pos + 1:next_pos]
                left_subresult = _evaluate(tokens, pos + 1)
                operators = tokens[next_pos]
                right_operators = tokens[next_pos + 1:]
                if operators != ')' or (left_operators and (not all((o == operators for o in left_operators)))):
                    raise ValueError('Invalid expression')
                right_subresult = _evaluate(tokens, next_pos + 1)
                if operators == '/':
                    result = int(left_subresult / right_subresult // 1)
                else:
                    right_operators = list(reversed(right_operators))
                    for operator in right_operators:
                        if operator in {'+', '-'}:
                            if left_operators and left_operators[-1] == operator:
                                left_operators.pop()
                                break
                            else:
                                result = operator == '+' and left_subresult + right_subresult or left_subresult - right_subresult
                                break
        return result
    tokens = expr.replace(' ', '').split(')')[0].split('(')[-1].split('+')
    tokens += ['+'] + [')']
    _evaluate(tokens)