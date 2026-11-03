def search_insert_position(nums, target):
    """
    Searches for the target in a sorted list and returns its index.
    If not found, returns the insertion point.

    Args:
        nums (list): A sorted list of numbers.
        target (int): The value to be searched.

    Returns:
        int: Index if target is found, else insertion point.

    Raises:
        ValueError: If input list is empty or None.
    """
    if not isinstance(nums, list) or len(nums) == 0:
        raise ValueError('Input must be a non-empty list.')
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