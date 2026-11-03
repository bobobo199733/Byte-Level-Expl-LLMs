def find_kth(nums1, nums2, k):
    if len(nums1) > len(nums2):
        return find_kth(nums2, nums1, k)
    m, n = (len(nums1), len(nums2))
    imin, imax = (0, min(k, m))
    while imin <= imax:
        i = (imin + imax) // 2
        j = k - i
        if i < m and nums1[i] < nums2[j - 1]:
            imin = i + 1
        elif i > 0 and nums1[i - 1] > nums2[j]:
            imax = i - 1
        else:
            if i == 0:
                max_of_left = nums2[j - 1]
            elif j == 0:
                max_of_left = nums1[i - 1]
            else:
                max_of_left = max(nums1[i - 1], nums2[j - 1])
            if (m + n) % 2 == 1:
                return max_of_left
            if i == m:
                min_of_right = nums2[j]
            elif j == n:
                min_of_right = nums1[i]
            else:
                min_of_right = min(nums1[i], nums2[j])
            return (max_of_left + min_of_right) / 2.0

def median_of_two_sorted_arrays(nums1, nums2):
    total_length = len(nums1) + len(nums2)
    if total_length % 2 == 1:
        return find_kth(nums1, nums2, total_length // 2 + 1)
    else:
        return (find_kth(nums1, nums2, total_length // 2) + find_kth(nums1, nums2, total_length // 2 + 1)) / 2.0