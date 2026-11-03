def fast_power(base: int, exponent: int) -> int:
    """
    Compute base raised to exponent using exponentiation by squaring.

    Args:
        base (int): The base number
        exponent (int): The exponent

    Returns:
        int: The result of base raised to exponent
    """

    def power(base: int, exponent: int) -> int:
        if exponent == 0:
            return 1
        half_pow = power(base, exponent // 2)
        if exponent % 2 == 0:
            return half_pow * half_pow
        else:
            return base * half_pow * half_pow
    return power(base, exponent)