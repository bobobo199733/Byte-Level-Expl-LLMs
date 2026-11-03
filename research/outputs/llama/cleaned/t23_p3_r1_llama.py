def fast_power(base, exponent):
    """
    Quickly compute base to the exponent.

    Args:
        base (int): The base number.
        exponent (int): The power to which the base is raised.

    Returns:
        int: The result of base to the exponent.
    """
    if exponent == 0:
        return 1
    if exponent < 0:
        base = 1 / base
        exponent = -exponent
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result *= base
        base *= base
        exponent //= 2
    return result