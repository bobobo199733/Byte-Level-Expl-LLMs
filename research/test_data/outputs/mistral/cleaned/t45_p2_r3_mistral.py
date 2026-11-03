def search_insert_position(nums, target):
    if not nums or isinstance(nums, list) is False:
        raise ValueError('Input must be a non-empty sorted list.')
    left, right = (0, len(nums) - 1)
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left