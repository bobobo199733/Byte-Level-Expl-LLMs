def quickselect(nums, left, right, k):
    if left == right:
        return nums[left]
    pivot_index = (left + right) // 2
    pivot = nums[pivot_index]
    smaller_elements_index = left - 1
    store_index = left
    for i in range(left, right + 1):
        if nums[i] <= pivot:
            smaller_elements_index += 1
            nums[smaller_elements_index], nums[i] = (nums[i], nums[smaller_elements_index])
            nums[store_index], nums[i] = (nums[i], nums[store_index])
            store_index += 1
    if k == smaller_elements_index + 1:
        return quickselect(nums, left, store_index - 1, k)
    elif k > smaller_elements_index + 1:
        return quickselect(nums, store_index + 1, right, k)
    else:
        return quickselect(nums, left, store_index, k)

def kth_largest(nums, k):
    return quickselect(sorted(set(nums), reverse=True), 0, len(nums) - 1, len(nums) - k)