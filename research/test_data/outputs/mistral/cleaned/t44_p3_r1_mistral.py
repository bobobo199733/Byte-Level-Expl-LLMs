def rotate_array(nums, k):
    n = len(nums)
    k %= n
    reversed_part1 = nums[-k:] + nums[:-k]
    reversed_part2 = nums[n - k:]
    nums[len(reversed_part1):] = reversed_part1[::-1]
    nums[:n - len(reversed_part2)] = reversed_part2[::-1]