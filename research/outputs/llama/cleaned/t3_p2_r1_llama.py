def evaluate(expr: str) -> int:
    """
    Evaluate an arithmetic expression string containing integers, +, -, *, /, and parentheses.

    Args:
        expr (str): The arithmetic expression to be evaluated.

    Returns:
        int: The integer result of the evaluation.
    """
    result = eval(expr)
    return int(result) if isinstance(result, (int, float)) else 'Invalid input'