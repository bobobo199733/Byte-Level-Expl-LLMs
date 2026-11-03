def median_of_two_sorted_arrays(nums1, nums2):
    m = len(nums1)
    n = len(nums2)
    if m > n:
        nums1, nums2 = (nums2, nums1)
        m, n = (n, m)
    x_min, x_max = (0, m)
    for i in range(m + n + 1):
        partition = (x_max + x_min) // 2
        left1 = max(0, partition - m // 2) if partition >= m / 2 else 0
        right1 = min(partition, m)
        left2 = partition - right1
        if left1 > right1:
            x_max = partition - 1
        elif left2 > right2:
            x_min = partition + 1
        else:
            index1 = left1
            index2 = left2
            total = right1 + right2
            if total == m + n:
                return sorted([nums1[index1], nums2[index2]])[1]
            elif total > m + n:
                x_min = partition + 1
            else:
                x_max = partition - 1
    if m == n:
        return sorted(nums1 + nums2)[m // 2]
    mid1 = x_min + (m - x_max) // 2
    mid2 = x_min + (n - x_max) // 2
    return sum(sorted([nums1[mid1], nums2[mid2]])) / 2