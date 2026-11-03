def kth_largest(nums, k):
    """
    Returns the kth largest element in a list.

    Args:
        nums (list): A list of integers.
        k (int): The position of the largest element to return (1-indexed).

    Returns:
        int: The kth largest element in the list.
    """
    return sorted(nums, reverse=True)[k - 1]