def search_insert_position(nums, target):
    """
    Returns the correct index or insertion position of the target value in a sorted array.

    Args:
        nums (list): A sorted list of integers.
        target (int): The target value to be searched.

    Returns:
        int: The index where the target value should be inserted to maintain sorted order.
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