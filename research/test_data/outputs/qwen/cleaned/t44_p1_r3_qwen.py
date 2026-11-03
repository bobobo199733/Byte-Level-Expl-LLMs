def rotate_array(nums, k):
    n = len(nums)
    k %= n
    return nums[-k:] + nums[:-k]