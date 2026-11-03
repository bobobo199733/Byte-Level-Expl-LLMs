def count_set_bits(n):
    """
    Counts the number of set (1) bits in a given integer.

    Args:
        n (int): The input integer.

    Returns:
        int: The number of set bits in n.
    """
    binary_str = bin(n)[2:]
    count = binary_str.count('1')
    return count