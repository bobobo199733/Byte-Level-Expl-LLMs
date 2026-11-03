import heapq

def kth_largest(nums, k):
    """
    Returns the kth largest number in the list nums.

    Args:
        nums (list): A list of numbers.
        k (int): The position of the number to be found.

    Returns:
        int: The kth largest number in the list.
    """
    if k < 1 or k > len(nums):
        raise ValueError('k is out of range')
    return heapq.nlargest(k, nums)[-1]