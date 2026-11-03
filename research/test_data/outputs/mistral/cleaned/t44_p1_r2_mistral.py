def rotate_array(nums, k):
    n = len(nums)
    k %= n
    original = nums[:]
    reversed_first = nums[-k:][::-1]
    reversed_last = nums[:n - k][::-1]
    rotated = reversed_first + original[k:] + reversed_last
    return rotated