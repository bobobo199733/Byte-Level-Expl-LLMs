def binary_search_rotated(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        mid = (low + high) // 2
        if values[mid] == target:
            return mid
        if values[low] <= values[mid]:
            if target < values[low] or target > values[mid]:
                low += 1
        elif target >= values[high] and target < values[mid]:
            high -= 1
        elif target < values[low]:
            high = mid - 1
        if low > high:
            return -1
    return -1