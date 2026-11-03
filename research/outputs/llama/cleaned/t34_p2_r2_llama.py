def binary_search_rotated(values, target):
    """
    Searches for a target value inside a rotated sorted array using binary search principles.

    Args:
        values (list): A rotated sorted list of integers.
        target (int): The number to be searched in the array.

    Returns:
        int: Index of the target if it exists. -1 otherwise.

    Raises:
        TypeError: If input is not a list or integer.
    """
    if not isinstance(values, list) or not all((isinstance(num, (int, float)) for num in values)):
        raise TypeError("Input 'values' must be a list of integers")
    if not isinstance(target, (int, float)):
        raise TypeError("Input 'target' must be an integer")
    if len(values) == 0:
        return -1
    left = 0
    right = len(values) - 1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        elif values[left] <= values[mid]:
            if values[left] <= target < values[mid]:
                right = mid - 1
            else:
                left = mid + 1
        elif values[mid] < target <= values[right]:
            left = mid + 1
        else:
            right = mid - 1
    return -1