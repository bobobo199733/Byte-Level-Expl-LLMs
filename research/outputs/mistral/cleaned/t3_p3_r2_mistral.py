def operator_precedence(op):
    return {'+': 1, '-': 1, '*': 2, '/': 2}[op]

def evaluate(expr: str) -> int:

    def _eval(token):
        if token.isdigit():
            return int(token)
        elif token == '(':
            return _subexpr(token + '+')
        elif token == ')':
            return _subexpr(token + '-')
        elif (op := next((op for op in ('+', '-', '*', '/') if token.startswith(op)), None)):
            right = _eval(tokens.pop(0))
            left = _eval(tokens.pop(0))
            return {'+': left + right, '-': left - right, '*': left * right, '/': int(left / right)}[op]
        else:
            raise ValueError(f"Invalid token '{token}' in expression")
    tokens = list(filter(lambda x: x != ' ', expr))
    _subexpr = lambda op: _eval(next((token for token in reversed(tokens) if token.startswith(op)), None))
    return _eval(tokens[-1])