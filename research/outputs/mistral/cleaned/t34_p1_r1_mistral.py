def binary_search_rotated(values, target):
    left, right = (0, len(values) - 1)
    while left <= right:
        mid = (left + right) // 2
        mid_value = values[mid]
        if mid_value == target:
            return mid
        if values[left] <= mid_value and mid_value > values[right]:
            pivot = mid
        elif values[left] <= mid_value <= values[right]:
            right = mid - 1
        else:
            left = mid + 1
    return -1