def median_of_two_sorted_arrays(nums1, nums2):
    """
    Finds the median of two sorted arrays.

    Args:
        nums1 (list): The first sorted array.
        nums2 (list): The second sorted array.

    Returns:
        float: The median of the combined array.
    """
    if len(nums1) > len(nums2):
        nums1, nums2 = (nums2, nums1)
    total_len = len(nums1) + len(nums2)
    half_len = total_len // 2
    left, right = (0, len(nums1))
    while left <= right:
        i = (left + right) // 2
        j = half_len - i
        max_left_x = float('-inf') if i == 0 else nums1[i - 1]
        min_right_x = float('inf') if i == len(nums1) else nums1[i]
        max_left_y = float('-inf') if j == 0 else nums2[j - 1]
        min_right_y = float('inf') if j == len(nums2) else nums2[j]
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            if total_len % 2:
                return min(min_right_x, min_right_y)
            else:
                return (max(max_left_x, max_left_y) + min(min_right_x, min_right_y)) / 2
        elif max_left_x > min_right_y:
            right = i - 1
        else:
            left = i + 1