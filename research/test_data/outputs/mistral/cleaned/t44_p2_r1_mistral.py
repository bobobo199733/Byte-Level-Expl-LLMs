def rotate_array(nums, k):
    if not isinstance(nums, list) or k < 0 or len(nums) <= k:
        raise ValueError('Invalid input')
    n = len(nums)
    k %= n
    result = [None] * n
    for i in range(n):
        j = (i + k) % n
        result[j] = nums[i]
    return result