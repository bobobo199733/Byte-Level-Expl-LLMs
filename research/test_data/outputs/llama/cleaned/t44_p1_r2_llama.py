def rotate_array(nums, k):
    """
    Rotate an array to the right by k steps.

    Args:
        nums (list): The input list to be rotated.
        k (int): The number of steps to rotate the array.

    Returns:
        list: The rotated array.
    """
    k = k % len(nums)
    nums.reverse()
    nums[:k] = nums[:k][::-1]
    nums[k:] = nums[k:][::-1]
    return nums