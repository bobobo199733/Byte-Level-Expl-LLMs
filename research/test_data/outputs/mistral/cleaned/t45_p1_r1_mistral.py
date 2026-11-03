def search_insert_position(nums, target):
    if len(nums) == 0:
        return 0
    left, right = (0, len(nums) - 1)
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    if nums[-1] < target:
        return len(nums)
    for i in range(len(nums)):
        if nums[i] >= target:
            return i