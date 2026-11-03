def merge_sorted(nums1, nums2):
    merged = sorted(nums1 + nums2)
    return merged[len(merged) // 2] if len(merged) % 2 == 0 else (merged[(len(merged) - 1) // 2] + merged[len(merged) // 2]) / 2

def median_of_two_sorted_arrays(nums1, nums2):
    return merge_sorted(nums1, nums2)