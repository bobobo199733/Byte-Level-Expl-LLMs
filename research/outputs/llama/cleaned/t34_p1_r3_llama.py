def binary_search_rotated(values, target):
    """
    Searches for a target in a rotated sorted array using binary search.

    Args:
        values (list): A rotated sorted list of numbers.
        target: The number to find.

    Returns:
        int: Index of the target if found; -1 otherwise.
    """
    if not values:
        return -1
    low = 0
    high = len(values) - 1
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