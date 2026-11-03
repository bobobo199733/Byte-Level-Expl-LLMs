def binary_search_rotated(values, target):
    """
    Searches for a target value in a rotated sorted array using binary search.
    
    Args:
    values (List[int]): A rotated sorted array of integers.
    target (int): The integer to be searched in the array.
    
    Returns:
    int: The index of the target if found, otherwise -1.
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