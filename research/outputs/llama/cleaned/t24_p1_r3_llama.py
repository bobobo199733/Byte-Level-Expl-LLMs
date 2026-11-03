def kth_largest(nums, k):
    """
    Returns the kth largest element in a list.

    Args:
        nums (list): A list of numbers.
        k (int): The index of the largest element to return (1-indexed).

    Returns:
        int: The kth largest element in the list.
    """
    return sorted(nums, reverse=True)[k - 1]