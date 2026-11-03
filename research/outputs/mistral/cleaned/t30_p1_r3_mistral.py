def max_subarray_sum(nums):
    if not nums:
        return 0
    current_max = nums[0]
    global_max = nums[0]
    for num in nums[1:]:
        current_max = max(num, current_max + num)
        global_max = max(current_max, global_max)
    return global_max