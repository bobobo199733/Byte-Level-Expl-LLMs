def rotate_array(nums, k):
    if len(nums) == 0 or k < 0:
        raise ValueError('Invalid input')
    k %= len(nums)
    return nums[-k:] + nums[:-k]