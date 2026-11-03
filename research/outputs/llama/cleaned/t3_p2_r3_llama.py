def evaluate(expr: str) -> int:
    """
    Evaluate an arithmetic expression string containing integers, +, -, *, /, and parentheses.

    Args:
        expr (str): The arithmetic expression to be evaluated.

    Returns:
        int: The integer result of the evaluation.
    """
    expr = expr.replace(' ', '')
    try:
        result = eval(expr)
        if not isinstance(result, int):
            raise ValueError(f'Expected integer result, but got {result} of type {type(result)}')
        return result
    except SyntaxError as e:
        raise ValueError(f'Invalid expression: {expr}') from e
    except ZeroDivisionError as e:
        raise ValueError(f'Division by zero: {expr}') from e