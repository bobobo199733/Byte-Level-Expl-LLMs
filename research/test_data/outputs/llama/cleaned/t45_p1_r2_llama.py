def search_insert_position(nums, target):
    """
    Returns the index of the target in a sorted array. 
    If the target does not exist, returns the index where it should be inserted.

    Args:
        nums (list): A sorted list of integers.
        target (int): The number to be searched for.

    Returns:
        int: The index of the target or its insertion position.
    """
    left, right = (0, len(nums) - 1)
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left