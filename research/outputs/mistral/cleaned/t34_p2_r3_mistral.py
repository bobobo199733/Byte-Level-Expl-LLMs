def binary_search_rotated(values, target):

    def is_rotated(arr):
        return arr[0] > arr[-1]
    if not values or (len(values) == 1 and values[0] != target):
        return -1
    left, right = (0, len(values) - 1)
    if not is_rotated(values):
        while left <= right:
            mid = (left + right) // 2
            if values[mid] == target:
                return mid
            elif values[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] > values[left]:
            min_value_range = left
        elif values[mid] < values[left]:
            min_value_range = mid
        else:
            min_value_range = left + 1
        if target >= values[min_value_range] and target <= values[right]:
            while left < right:
                mid = (left + right) // 2
                if values[mid] == target:
                    return mid
                elif values[mid] > target:
                    right = mid
                else:
                    left = mid + 1
            return -1
        elif values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1