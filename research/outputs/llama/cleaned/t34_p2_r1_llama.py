def binary_search_rotated(values, target):
    """
    Searches for the given target value inside a rotated sorted array.

    Args:
        values (list): A rotated sorted list of integers.
        target (int): The target integer to be searched within the array.

    Returns:
        int: The index of the target if it exists. Otherwise returns -1.

    Raises:
        TypeError: If either 'values' or 'target' are not of correct type.
    """
    if not isinstance(values, list) or not all((isinstance(x, int) for x in values)):
        raise TypeError("Invalid input: 'values' should be a list of integers.")
    if not isinstance(target, int):
        raise TypeError("Invalid input: 'target' should be an integer.")
    if len(values) == 0:
        return -1
    left = 0
    right = len(values) - 1
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