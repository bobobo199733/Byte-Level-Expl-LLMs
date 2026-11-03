def search_insert_position(nums, target):
    """
    Searches for the target in a sorted array and returns its index. 
    If the target does not exist, it returns the index where it should be inserted.

    Args:
        nums (list): A sorted list of numbers.
        target (int): The number to be searched.

    Returns:
        int: The index of the target in the array or the index where it should be inserted.

    Example:
        >>> search_insert_position([1, 3, 5, 6], 5)
        2
        >>> search_insert_position([1, 3, 5, 6], 2)
        1
        >>> search_insert_position([1, 3, 5, 6], 7)
        4
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