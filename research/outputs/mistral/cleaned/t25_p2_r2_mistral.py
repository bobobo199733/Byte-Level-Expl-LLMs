def count_set_bits(n):
    if n < 0:
        raise ValueError('Input should be non-negative')
    count = 0
    while n > 0:
        n &= n - 1
        count += 1
    return count