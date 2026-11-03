def fast_power(base, exponent):
    if exponent == 0:
        return 1
    elif exponent % 2 == 0:
        return fast_power(base * base, int(exponent / 2))
    else:
        return base * fast_power(base, exponent - 1)