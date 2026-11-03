def rotate_array(nums, k):
    """
    Rotates the given list 'nums' to the right by 'k' positions.

    :param nums: List of integers or other elements.
    :param k: Number of positions to rotate the array to the right.
    :return: The rotated list.
    """
    n = len(nums)
    k = k % n
    if k == 0:
        return nums
    return nums[-k:] + nums[:-k]