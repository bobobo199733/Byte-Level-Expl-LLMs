import ast

def evaluate(expr: str) -> int:
    try:
        expression = ast.parse(expr, mode='eval')
        result = eval(compile(expression, '<string>', 'eval'))
        return int(result)
    except Exception as e:
        print(f'Error evaluating the expression: {str(e)}')
        return None