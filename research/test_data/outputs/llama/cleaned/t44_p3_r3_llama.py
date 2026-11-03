def rotate_array(nums, k):
    """
    Rotate the input array to the right by k positions.

    Args:
        nums (list): The input array.
        k (int): The number of positions to rotate.

    Returns:
        list: The rotated array.
    """
    if len(nums) == 0 or k == 0:
        return nums
    k = k % len(nums)
    return nums[-k:] + nums[:-k]