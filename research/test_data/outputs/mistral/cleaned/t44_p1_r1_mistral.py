def rotate_array(nums, k):
    k %= len(nums)
    nums[:len(nums) - k] = reversed(nums[:len(nums) - k])
    nums[len(nums) - k:] = reversed(nums[len(nums) - k:])
    nums = list(reversed(nums))
    return nums