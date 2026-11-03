def median_of_two_sorted_arrays(nums1, nums2):
    """
    Calculate the median of two sorted arrays efficiently using binary search.

    Args:
        nums1 (list): The first sorted array.
        nums2 (list): The second sorted array.

    Returns:
        float: The median of the combined arrays.
    """
    if len(nums1) > len(nums2):
        nums1, nums2 = (nums2, nums1)
    total_length = len(nums1) + len(nums2)
    half_length = total_length // 2
    left, right = (0, len(nums1) - 1)
    while True:
        i = (left + right) // 2
        j = half_length - i - 2
        nums1_left = nums1[i + 1] if i < len(nums1) else float('-infinity')
        nums1_right = nums1[i] if i >= 0 else float('inf')
        nums2_left = nums2[j + 1] if j < len(nums2) else float('-infinity')
        nums2_right = nums2[j] if j >= 0 else float('inf')
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            if total_length % 2 == 0:
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2.0
            else:
                return max(min(nums1_right, nums2_right), max(nums1_left, nums2_left))
        elif nums1_left > nums2_right:
            right = i - 1
        else:
            left = i + 1