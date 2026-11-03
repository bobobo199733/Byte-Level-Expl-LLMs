def count_set_bits(n):
    """
    Counts how many bits are set to 1 in a non-negative integer.

    Args:
        n (int): The non-negative integer to be counted.

    Returns:
        int: The number of bits set to 1.

    Raises:
        ValueError: If the input is negative.
    """
    if n < 0:
        raise ValueError('Input must be a non-negative integer.')
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1
    return count