def binary_search_rotated(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        mid = (low + high) // 2
        if values[mid] == target or values[low] <= values[mid] <= values[high]:
            return mid
        elif values[mid] > values[high]:
            high = mid - 1
        else:
            low = mid + 1
    return -1