def binary_search_rotated(values, target):

    def find_pivot(arr, low, high):
        if low == high:
            return low
        mid = (low + high) // 2
        if arr[mid] > arr[mid + 1]:
            return mid
        if arr[low] <= arr[mid] >= arr[high]:
            return find_pivot(arr, mid + 1, high)
        return find_pivot(arr, low, mid)
    pivot = find_pivot(values, 0, len(values) - 1)
    if not values:
        return -1
    left_part = values[:pivot]
    right_part = values[pivot:]
    if target < left_part[-1] <= target < right_part[0]:
        return -1
    if target < left_part[-1]:
        return binary_search(left_part, target)
    return binary_search(right_part, target) + pivot

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1