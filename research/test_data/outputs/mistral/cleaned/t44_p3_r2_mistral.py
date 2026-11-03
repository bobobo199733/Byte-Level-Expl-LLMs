def rotate_array(nums, k):
    nums += nums[:k]
    del nums[0:k]
    return nums