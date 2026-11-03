def fast_power(base, exponent):
    result = 1
    while exponent > 0:
        if exponent & 1:
            result *= base
        base *= base
        exponent >>= 1
    return result