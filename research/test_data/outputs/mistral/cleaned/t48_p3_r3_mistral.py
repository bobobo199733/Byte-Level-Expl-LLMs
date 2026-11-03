def median_of_two_sorted_arrays(nums1, nums2):
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n == 0:
        return float('nan')
    if n % 2 == 0:
        median_index = (n - 1) // 2
        left_median = merged[median_index]
        right_median = merged[median_index + 1]
        return (left_median + right_median) / 2
    else:
        median_index = n // 2
        median = merged[median_index]
        return median