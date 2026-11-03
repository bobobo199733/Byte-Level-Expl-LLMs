def max_subarray_sum(nums):
    if not nums:
        raise ValueError('Input list cannot be empty')
    current_sum = max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum