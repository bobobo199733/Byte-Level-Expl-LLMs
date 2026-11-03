def median_of_two_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        return median_of_two_sorted_arrays(nums2, nums1)
    m, n = (len(nums1), len(nums2))
    imin, imax = (0, m)
    while imin <= imax:
        i = (imin + imax) // 2
        j = (m + n + 1) // 2 - i
        if i < m and nums2[j - 1] > nums1[i]:
            imin = i + 1
        elif i > 0 and nums1[i - 1] > nums2[j]:
            imax = i - 1
        else:
            if i == 0:
                max_left = float('-inf')
            else:
                max_left = nums1[i - 1]
            if j == 0:
                min_right = float('inf')
            else:
                min_right = nums2[j - 1]
            if (m + n) % 2 == 1:
                return float(max_left)
            return (max_left + min_right) / 2.0