def kth_largest(nums, k):
    """
    Find the k-th largest element in the given list.

    Parameters:
    nums (list): A list of integers.
    k (int): The k-th position to find the largest element for.

    Returns:
    int: The k-th largest element in the list.
    """
    return sorted(nums, reverse=True)[k - 1]