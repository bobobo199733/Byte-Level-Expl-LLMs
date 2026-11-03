def count_set_bits(n):
    if n < 0:
        raise ValueError('Input must be a non-negative integer')
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count