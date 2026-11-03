def binary_search_rotated(values, target):
    if not values:
        return -1
    left, right = (0, len(values) - 1)
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[left] < values[mid]:
            if values[left] <= target < values[mid]:
                right = mid - 1
            else:
                left = mid + 1
        elif values[mid] < values[right]:
            if values[mid] < target <= values[right]:
                left = mid + 1
            else:
                right = mid - 1
        elif values[left] == values[mid]:
            left += 1
        else:
            right -= 1
    return -1