def find_kth_element(arr1, arr2, k):
    if len(arr1) > len(arr2):
        arr1, arr2 = (arr2, arr1)
    m, n = (len(arr1), len(arr2))
    imin, imax = (0, m)
    while imin <= imax:
        i = (imin + imax) // 2
        j = k - i
        if i < m and arr2[j - 1] > arr1[i]:
            imin = i + 1
        elif i > 0 and arr1[i - 1] > arr2[j]:
            imax = i - 1
        else:
            if i == 0:
                max_of_left = arr2[j - 1]
            elif j == 0:
                max_of_left = arr1[i - 1]
            else:
                max_of_left = max(arr1[i - 1], arr2[j - 1])
            if m + n % 2 == 1:
                return max_of_left
            if i == m:
                min_of_right = arr2[j]
            elif j == n:
                min_of_right = arr1[i]
            else:
                min_of_right = min(arr1[i], arr2[j])
            return (max_of_left + min_of_right) / 2.0

def median_of_two_sorted_arrays(nums1, nums2):
    total_length = len(nums1) + len(nums2)
    if total_length % 2 == 1:
        return find_kth_element(nums1, nums2, total_length // 2 + 1)
    else:
        return (find_kth_element(nums1, nums2, total_length // 2) + find_kth_element(nums1, nums2, total_length // 2 + 1)) / 2.0