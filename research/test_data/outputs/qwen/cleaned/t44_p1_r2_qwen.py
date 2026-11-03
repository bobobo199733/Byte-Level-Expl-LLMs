def rotate_array(nums, k):
    n = len(nums)
    k = k % n
    if k == 0:
        return nums
    rotated_part = nums[-k:]
    non_rotated_part = nums[:-k]
    return rotated_part + non_rotated_part