def binary_search_rotated(values, target):
    """
    Searches for a target in a rotated sorted array using binary search.

    Args:
        values (list): The rotated sorted array.
        target: The value to be searched.

    Returns:
        int: Index of the target if found. -1 otherwise.
    """
    left, right = (0, len(values) - 1)
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[left] <= values[mid]:
            if values[left] <= target < values[mid]:
                right = mid - 1
            else:
                left = mid + 1
        elif values[mid] < target <= values[right]:
            left = mid + 1
        else:
            right = mid - 1
    return -1