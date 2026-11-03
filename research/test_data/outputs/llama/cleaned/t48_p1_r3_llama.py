def median_of_two_sorted_arrays(nums1, nums2):
    """
    Find the median of two sorted arrays.

    Args:
        nums1 (list): First sorted array.
        nums2 (list): Second sorted array.

    Returns:
        float: The median of the combined array.
    """
    if len(nums1) > len(nums2):
        nums1, nums2 = (nums2, nums1)
    total_length = len(nums1) + len(nums2)
    half_length = total_length // 2
    left, right = (0, len(nums1) - 1)
    while True:
        i = (left + right) // 2
        j = half_length - i - 2
        nums1_left = float('-inf') if i < 0 else nums1[i]
        nums1_right = float('inf') if i >= len(nums1) - 1 else nums1[i + 1]
        nums2_left = float('-inf') if j < 0 else nums2[j]
        nums2_right = float('inf') if j >= len(nums2) - 1 else nums2[j + 1]
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            if total_length % 2 == 1:
                return float(min(nums1_right, nums2_right))
            else:
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2
        elif nums1_left > nums2_right:
            right = i - 1
        else:
            left = i + 1