def search_insert_position(nums, target):
    """
    Returns the index of the target in a sorted list.
    If not found, returns the insertion position.

    Args:
        nums (list): A sorted list of integers.
        target (int): The value to be searched.

    Raises:
        ValueError: If input is invalid.

    Returns:
        int: Index or insertion position.
    """
    if not isinstance(nums, list) or len(nums) == 0 or (not all((isinstance(x, int) for x in nums))):
        raise ValueError('Invalid input')
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