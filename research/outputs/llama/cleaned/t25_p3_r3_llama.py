def count_set_bits(n):
    """
    This function takes an integer as input and returns the number of set bits (i.e., bits with value 1) in its binary representation.

    Args:
        n (int): The input integer.

    Returns:
        int: The number of set bits in the binary representation of n.
    """
    return bin(n).count('1')