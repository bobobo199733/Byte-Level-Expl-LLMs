def kth_largest(nums, k):
    """
    Returns the kth largest value from a list of numbers.

    Args:
        nums (list): A list of integers.
        k (int): The position of the number to be returned.

    Returns:
        int: The kth largest number in the list.

    Raises:
        ValueError: If k is invalid (less than 1 or larger than the length of the list).
    """
    if not isinstance(nums, list) or not all((isinstance(x, int) for x in nums)):
        raise TypeError('nums must be a list of integers')
    if not isinstance(k, int) or k < 1 or k > len(nums):
        raise ValueError('k is invalid')
    return sorted(nums, reverse=True)[k - 1]