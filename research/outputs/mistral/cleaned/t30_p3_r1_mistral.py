def max_subarray_sum(nums):
    if not nums:
        return None
    current_max = nums[0]
    global_max = nums[0]
    current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        if current_sum > global_max:
            global_max = current_sum
    return global_max