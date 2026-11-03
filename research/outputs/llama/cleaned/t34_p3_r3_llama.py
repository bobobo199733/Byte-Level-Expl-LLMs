def binary_search_rotated(values, target):
    """
    Searches a rotated sorted list for a target value using binary search algorithm.

    Args:
        values (list): A list of numbers that is initially sorted but has been rotated at some point.
        target (int): The number to be searched in the list.

    Returns:
        int: Index of the target value if it exists, -1 otherwise.
    """
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