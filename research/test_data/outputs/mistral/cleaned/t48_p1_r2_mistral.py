def median_of_two_sorted_arrays(nums1, nums2):
    m, n = (len(nums1), len(nums2))
    if m > n:
        nums1, nums2 = (nums2, nums1)
        m, n = (n, m)
    low_pointer = 0
    high_pointer_nums1 = m - 1
    high_pointer_nums2 = n - 1
    while True:
        low_pointer_nums1 = (high_pointer_nums1 + low_pointer) // 2
        low_pointer_nums2 = (high_pointer_nums2 + low_pointer) // 2
        if nums1[low_pointer_nums1] <= nums2[low_pointer_nums2]:
            low_pointer = low_pointer_nums1 + 1
            high_pointer_nums2 = low_pointer_nums2 - 1
        else:
            high_pointer_nums1 = low_pointer_nums1 - 1
            high_pointer_nums2 = low_pointer_nums2 + 1
        if high_pointer_nums1 == low_pointer_nums2:
            if m + n % 2 != 0:
                return nums1[low_pointer_nums1]
            else:
                return (nums1[low_pointer_nums1] + nums2[low_pointer_nums2]) / 2.0
        if high_pointer_nums1 < low_pointer_nums1 or high_pointer_nums2 < low_pointer_nums2:
            if m + n % 2 != 0:
                return nums1[low_pointer_nums1] if high_pointer_nums1 >= low_pointer_nums1 else nums2[low_pointer_nums2]
            else:
                return (nums1[high_pointer_nums1] + nums2[high_pointer_nums2]) / 2.0