def kth_largest(nums, k):
    if len(nums) < k or k <= 0:
        raise ValueError('Invalid value for k')
    nums = sorted(nums, reverse=True)
    return nums[k - 1]