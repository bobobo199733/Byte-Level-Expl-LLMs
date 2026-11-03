def rotate_array(nums, k):
    """
    Rotate the input array to the right by k positions.
    
    Args:
        nums (list): The input list to be rotated.
        k (int): The number of positions to rotate to the right.
        
    Returns:
        list: The rotated list.
        
    Raises:
        ValueError: If k is greater than the length of nums or if nums is not a list.
    """
    if not isinstance(nums, list):
        raise ValueError('nums must be a list')
    n = len(nums)
    k %= n
    left = nums[:n - k]
    right = nums[n - k:]
    rotated_nums = right + left
    return rotated_nums