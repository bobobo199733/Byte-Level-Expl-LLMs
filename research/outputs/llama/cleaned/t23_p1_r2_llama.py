def fast_power(base: int, exponent: int) -> int:
    """
    Compute base raised to exponent efficiently using binary exponentiation.

    Args:
        base (int): The base number.
        exponent (int): The exponent.

    Returns:
        int: Base raised to the power of exponent.
    """
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result *= base
        base *= base
        exponent //= 2
    return result