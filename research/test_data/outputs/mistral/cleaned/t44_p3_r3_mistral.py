def rotate_array(nums, k):
    nums += nums[:k]
    nums[:k] = []
    return nums