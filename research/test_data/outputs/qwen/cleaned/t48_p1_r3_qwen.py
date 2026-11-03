def find_kth_smallest(nums1, nums2, k):
    """
    Helper function to find the k-th smallest element in two sorted arrays.
    This is used in a binary search approach to find the median efficiently.
    """
    len1, len2 = (len(nums1), len(nums2))
    if len1 > len2:
        return find_kth_smallest(nums2, nums1, k)
    left, right = (0, min(len1, k))
    while left < right:
        mid1 = (left + right) // 2
        mid2 = k - mid1
        if mid1 == 0:
            return nums2[mid2 - 1]
        if mid2 == 0:
            return nums1[mid1 - 1]
        l1 = nums1[mid1 - 1]
        l2 = nums2[mid2 - 1]
        if l1 > l2:
            right = mid1
        else:
            left = mid1 + 1
    i = left - 1
    j = k - left
    min_from_left = float('-inf') if i < 0 else nums1[i]
    max_from_right = float('inf') if j < 0 else nums2[j]
    return max(min_from_left, max_from_right)

def median_of_two_sorted_arrays(nums1, nums2):
    """
    Finds the median of two sorted arrays in O(log(m+n)) time complexity.
    
    :param nums1: List[int] - First sorted array
    :param nums2: List[int] - Second sorted array
    :return: float - Median of both arrays
    """
    total_length = len(nums1) + len(nums2)
    if total_length % 2 == 1:
        return find_kth_smallest(nums1, nums2, total_length // 2 + 1)
    else:
        return (find_kth_smallest(nums1, nums2, total_length // 2) + find_kth_smallest(nums1, nums2, total_length // 2 + 1)) / 2.0