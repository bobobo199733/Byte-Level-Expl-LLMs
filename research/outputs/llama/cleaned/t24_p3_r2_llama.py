import heapq

def kth_largest(nums, k):
    """
    Returns the kth largest number in the list.

    Args:
        nums (list): A list of integers.
        k (int): The index of the desired number from the end (1-indexed).

    Returns:
        int: The kth largest number in the list.
    """
    return heapq.nlargest(k, nums)[-1]