def kth_largest(nums, k):
    """
    Finds the k-th largest element in the list nums.

    :param nums: List of integers
    :param k: The order of the largest element to find (1st largest, 2nd largest, etc.)
    :return: The k-th largest element in the list
    """
    nums.sort(reverse=True)
    return nums[k - 1]