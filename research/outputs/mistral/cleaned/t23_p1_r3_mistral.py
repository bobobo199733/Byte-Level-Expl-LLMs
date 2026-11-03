def fast_power(base, exponent, power_table={}):
    if exponent == 0:
        return 1
    key = (base, exponent)
    if key in power_table:
        return power_table[key]
    result = base * fast_power(base, exponent - 1)
    power_table[key] = result
    return result