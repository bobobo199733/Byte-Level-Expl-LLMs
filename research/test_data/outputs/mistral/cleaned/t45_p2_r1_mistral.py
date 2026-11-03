def search_insert_position(nums, target):
    if not isinstance(nums, list) or not all((isinstance(i, (int, float)) for i in nums)):
        raise ValueError('Input list must contain only numbers.')
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left