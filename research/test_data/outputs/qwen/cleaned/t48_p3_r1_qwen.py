def find_kth_element(nums1, nums2, k):
    len1, len2 = (len(nums1), len(nums2))
    if len1 > len2:
        return find_kth_element(nums2, nums1, k)
    if not nums1:
        return nums2[k]
    if k == 0:
        return min(nums1[0], nums2[0])
    i = min(k // 2, len1 - 1)
    j = k - i
    if nums1[i] < nums2[j]:
        return find_kth_element(nums1[i + 1:], nums2[:j], k - (i + 1))
    else:
        return find_kth_element(nums1[:i], nums2[j:], k - i)

def median_of_two_sorted_arrays(nums1, nums2):
    total_length = len(nums1) + len(nums2)
    if total_length % 2 == 1:
        return find_kth_element(nums1, nums2, total_length // 2)
    else:
        return (find_kth_element(nums1, nums2, total_length // 2 - 1) + find_kth_element(nums1, nums2, total_length // 2)) / 2.0