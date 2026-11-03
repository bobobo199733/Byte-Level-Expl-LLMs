def fast_power(base, exponent):
    result = 1
    while exponent:
        if exponent % 2:
            result *= base
            exponent -= 1
        base *= base
        exponent //= 2
    return result