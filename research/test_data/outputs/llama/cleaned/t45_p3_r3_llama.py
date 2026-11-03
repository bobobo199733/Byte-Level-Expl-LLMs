def search_insert_position(nums, target):
    """
    Returns the correct index or insertion position in a sorted array.
    
    Args:
        nums (list): A sorted list of numbers.
        target (int): The number to be searched for.
        
    Returns:
        int: The correct index where the target should be inserted.
    """
    left, right = (0, len(nums) - 1)
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    return left