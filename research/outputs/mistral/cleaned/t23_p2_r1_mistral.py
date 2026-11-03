def fast_power(base, exponent):
    if exponent == 0:
        return 1
    elif exponent % 2 == 0:
        squared = fast_power(base * base, exponent // 2)
        return squared * squared if base >= 0 else squared * squared // base ** 2
    else:
        return base * fast_power(base * base, exponent - 1)