def binary_search_rotated(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        mid = (low + high) // 2
        if values[mid] == target:
            return mid
        elif values[low] <= values[mid]:
            if low < mid and values[mid] > values[mid + 1]:
                right_min = mid
            if values[low] <= target <= values[right_min]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if mid < high and values[mid] > values[high]:
                left_max = mid
            if values[left_max] <= target <= values[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1