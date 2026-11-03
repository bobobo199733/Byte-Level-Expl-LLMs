def rotate_array(nums, k):
    """
    Rotate an array to the right by k steps.

    Args:
        nums (list): The input array.
        k (int): The number of steps to rotate the array to the right.

    Returns:
        list: The rotated array.
    """
    k = k % len(nums)
    return nums[-k:] + nums[:-k]