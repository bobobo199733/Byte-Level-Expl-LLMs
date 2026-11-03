def rotate_array(nums, k):
    """
    Rotate the input array to the right by k steps.

    Args:
        nums (list): The input list of integers.
        k (int): The number of steps to rotate to the right.

    Returns:
        list: The rotated list.
    """
    k = k % len(nums)
    return nums[-k:] + nums[:-k]