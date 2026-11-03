def quickselect(nums, left, right, k):
    if left == right:
        return nums[left]
    pivot_index = (left + right) // 2
    pivot = nums[pivot_index]
    smaller = left - 1
    for i in range(left, right + 1):
        if nums[i] <= pivot:
            smaller += 1
            nums[smaller], nums[i] = (nums[i], nums[smaller])
    nums[right], nums[smaller + 1] = (nums[smaller + 1], nums[right])
    if k == smaller + 1:
        return nums[right]
    if k > smaller + 1:
        return quickselect(nums, right, smaller + 1, k)
    else:
        return quickselect(nums, left, smaller, k)

def kth_largest(nums, k):
    if len(nums) < k:
        raise ValueError('k must be less than or equal to the length of the list.')
    return quickselect(nums, 0, len(nums) - 1, len(nums) - k + 1)