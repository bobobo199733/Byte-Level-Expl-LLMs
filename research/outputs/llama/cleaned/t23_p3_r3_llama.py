def fast_power(base: int, exponent: int) -> float:
    """
    Quickly compute base to the power of exponent using exponentiation by squaring algorithm.

    Args:
        base (int): The base number.
        exponent (int): The power to which the base is raised.

    Returns:
        float: The result of base to the power of exponent.
    """
    if exponent == 0:
        return 1
    result = 1
    temp_base = abs(base)
    while exponent > 0:
        if exponent % 2 == 1:
            result *= temp_base
        temp_base *= temp_base
        exponent //= 2
    if base < 0:
        return -result
    return result