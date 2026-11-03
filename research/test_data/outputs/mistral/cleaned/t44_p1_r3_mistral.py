def rotate_array(nums, k):
    k = k % len(nums)
    nums_copy = nums[:]
    for i in range(k):
        start = len(nums) - 1
        end = 0
        temp = nums[end]
        while end < start:
            nums[end], nums[start] = (nums[start], nums[end])
            end += 1
            start -= 1
    return nums_copy