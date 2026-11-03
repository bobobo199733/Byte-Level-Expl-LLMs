def fast_power(base, exponent):
    if exponent == 0:
        return 1
    elif exponent % 2 == 0:
        half = fast_power(base, exponent // 2)
        return half * half
    else:
        return base * fast_power(base, exponent - 1)