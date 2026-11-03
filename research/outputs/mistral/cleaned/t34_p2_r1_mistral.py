def binary_search_rotated(values, target):
    if not values:
        return -1
    left, right = (0, len(values) - 1)
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if mid > 0 and values[mid] < values[mid - 1] or mid == 0:
            right = mid - 1
        else:
            left = mid + 1
    return -1