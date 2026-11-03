def rotate_array(nums, k):
    """
    Rotate the given list 'nums' to the right by 'k' steps.
    
    Parameters:
        nums (list): The input list of integers.
        k (int): Number of positions to rotate the array to the right.
        
    Returns:
        list: The rotated list.
    """
    n = len(nums)
    k %= n
    nums[:] = nums[-k:] + nums[:-k]
    return nums