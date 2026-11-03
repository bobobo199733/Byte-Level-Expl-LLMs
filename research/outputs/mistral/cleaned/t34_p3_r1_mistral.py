def binary_search_rotated(values, target):
    low = 0
    high = len(values) - 1
    if not values:
        return -1
    while low <= high:
        mid = (low + high) // 2
        if mid > 0 and values[mid] < values[mid - 1]:
            rotate_point = mid
        if values[mid] == target:
            return mid
        if values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1