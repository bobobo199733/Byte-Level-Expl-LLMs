def max_subarray_sum(nums):
    if not nums:
        raise ValueError('Input list cannot be empty')
    max_so_far = float('-inf')
    current_max = float('-inf')
    for num in nums:
        current_max = max(num, current_max + num)
        max_so_far = max(max_so_far, current_max)
    return max_so_far