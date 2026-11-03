def binary_search_rotated(values, target):
    """
    Searches for a target value inside a rotated sorted array.

    Args:
        values (list): The input array of integers.
        target (int): The target integer to find.

    Returns:
        int: Index of the target in the array if found. -1 otherwise.
    """
    if not values:
        return -1
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