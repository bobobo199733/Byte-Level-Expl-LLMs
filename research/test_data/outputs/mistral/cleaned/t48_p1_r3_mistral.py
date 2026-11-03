def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return _merge(left, right)

def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def median_of_two_sorted_arrays(nums1, nums2):
    total = len(nums1) + len(nums2)
    merged = merge_sort(nums1 + nums2)
    if total % 2 == 0:
        return (merged[len(nums1) // 2] + merged[len(nums1) // 2 + 1]) / 2
    else:
        return merged[len(nums1) // 2]