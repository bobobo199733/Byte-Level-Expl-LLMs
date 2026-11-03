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
        return int(eval(expr))
    except Exception as e:
        raise ValueError(f'Invalid arithmetic expression: {expr}. Error: {str(e)}')