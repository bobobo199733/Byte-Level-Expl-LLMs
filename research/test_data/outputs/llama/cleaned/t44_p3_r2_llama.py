def rotate_array(nums, k):
    """
    Rotate the input array to the right by k positions.

    Args:
        nums (list): The input list to be rotated.
        k (int): The number of positions to rotate the list.

    Returns:
        list: The rotated list.
    """
    k = k % len(nums)
    return nums[-k:] + nums[:-k]