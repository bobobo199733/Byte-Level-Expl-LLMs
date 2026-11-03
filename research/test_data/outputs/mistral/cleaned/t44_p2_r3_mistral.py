def rotate_array(nums, k):
    if not isinstance(nums, list) or len(nums) == 0:
        raise ValueError('Input should be a non-empty list.')
    if not isinstance(k, int) or k < 0:
        raise ValueError('k should be a positive integer.')
    n = len(nums)
    k %= n
    rotated_list = nums[-k:] + nums[:-k]
    return rotated_list