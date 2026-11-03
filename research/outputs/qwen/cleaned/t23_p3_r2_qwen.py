def fast_power(base, exponent):
    if exponent == 0:
        return 1
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result *= base
        base *= base
        exponent //= 2
    return result