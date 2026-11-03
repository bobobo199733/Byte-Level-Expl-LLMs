def rotate_array(nums, k):
    n = len(nums)
    if not isinstance(k, int) or k < 0 or k > n:
        raise ValueError('k must be a positive integer less than or equal to array length')
    k %= n
    result = nums[-k:] + nums[:-k]
    return result