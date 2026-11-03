import re

def evaluate(expr):
    expr = re.sub('\\s+', '', expr)
    try:
        return int(eval(expr))
    except Exception as e:
        return None