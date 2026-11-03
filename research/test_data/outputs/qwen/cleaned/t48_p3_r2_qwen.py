def find_kth_element(nums1, nums2, k):
    """
    Helper function to find the k-th smallest element from two sorted arrays.
    """
    len1, len2 = (len(nums1), len(nums2))
    if len1 > len2:
        return find_kth_element(nums2, nums1, k)
    start1, end1 = (0, len1)
    while start1 < end1:
        mid1 = (start1 + end1) // 2
        mid2 = k - mid1 - 1
        if mid1 >= len1:
            return nums2[mid2]
        elif mid2 < 0:
            return nums1[mid1]
        left1 = nums1[mid1] if mid1 > -1 else float('-inf')
        left2 = nums2[mid2] if mid2 > -1 else float('-inf')
        right1 = nums1[mid1 + 1] if mid1 + 1 < len1 else float('inf')
        right2 = nums2[mid2 + 1] if mid2 + 1 < len2 else float('inf')
        if left1 <= right2 and left2 <= right1:
            return max(left1, left2)
        elif left1 > right2:
            end1 = mid1 - 1
        else:
            start1 = mid1 + 1
    return float('-inf')

def median_of_two_sorted_arrays(nums1, nums2):
    """
    Finds the median of two sorted arrays using binary search.
    
    :param nums1: First sorted array.
    :param nums2: Second sorted array.
    :return: The median as a float.
    """
    total_length = len(nums1) + len(nums2)
    if total_length % 2 == 1:
        return find_kth_element(nums1, nums2, total_length // 2 + 1)
    else:
        return (find_kth_element(nums1, nums2, total_length // 2) + find_kth_element(nums1, nums2, total_length // 2 + 1)) / 2.0