def fast_power(base, exponent):
    """
    Quickly computes base to the exponent.

    Args:
        base (int): The base number.
        exponent (int): The power to which the base is raised.

    Returns:
        int: The result of base raised to the power of exponent.
    """
    if exponent == 0:
        return 1
    if exponent % 2 == 0:
        half_power = fast_power(base, exponent // 2)
        return half_power * half_power
    else:
        half_power = fast_power(base, (exponent - 1) // 2)
        return base * half_power * half_power