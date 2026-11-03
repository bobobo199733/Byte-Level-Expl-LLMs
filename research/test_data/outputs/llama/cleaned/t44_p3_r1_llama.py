def rotate_array(nums, k):
    """
    Rotate the input list to the right by k positions.

    Args:
        nums (list): The input list to be rotated.
        k (int): The number of positions to rotate to the right.

    Returns:
        list: The rotated list.
    """
    if len(nums) == 0 or k == 0:
        return nums
    k = k % len(nums)
    return nums[-k:] + nums[:-k]