def binary_search_rotated(values, target):
    """
    Searches for a target value in a rotated sorted list using binary search.

    Args:
        values (list): A rotated sorted list of integers.
        target (int): The value to be searched in the list.

    Returns:
        int: The index of the target value if found. -1 otherwise.
    """
    low, high = (0, len(values) - 1)
    while low <= high:
        mid = (low + high) // 2
        if values[mid] == target:
            return mid
        if values[low] <= values[mid]:
            if values[low] <= target < values[mid]:
                high = mid - 1
            else:
                low = mid + 1
        elif values[mid] < target <= values[high]:
            low = mid + 1
        else:
            high = mid - 1
    return -1