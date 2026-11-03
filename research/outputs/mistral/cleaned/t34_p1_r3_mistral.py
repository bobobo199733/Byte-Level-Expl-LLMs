def binary_search_rotated(values, target):
    low, high = (0, len(values) - 1)
    while low <= high:
        mid = (low + high) // 2
        if values[mid] == target:
            return mid
        if values[low] <= values[mid]:
            if target < values[mid] and target >= values[low]:
                high = mid - 1
            else:
                low = mid + 1
        elif target > values[mid] and target <= values[high]:
            low = mid + 1
        else:
            high = mid - 1
    return -1