def median_of_two_sorted_arrays(nums1, nums2):
    merged = sorted(nums1 + nums2)
    total_length = len(merged)
    if total_length == 0:
        return float('nan')
    mid_index = total_length // 2
    if total_length % 2 == 1:
        return merged[mid_index]
    else:
        return (merged[mid_index - 1] + merged[mid_index]) / 2