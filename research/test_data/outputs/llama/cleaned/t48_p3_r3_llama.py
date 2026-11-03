def median_of_two_sorted_arrays(nums1, nums2):
    """
    Find the median of two sorted arrays efficiently using binary search.

    Args:
        nums1 (list): The first sorted array.
        nums2 (list): The second sorted array.

    Returns:
        float: The median of the two arrays.

    Example:
        >>> median_of_two_sorted_arrays([1, 3], [2])
        2.0
    """
    if len(nums1) > len(nums2):
        nums1, nums2 = (nums2, nums1)
    x, y = (len(nums1), len(nums2))
    left, right = (0, x)
    while left <= right:
        i = (left + right) // 2
        j = (x + y + 1) // 2 - i
        max_left_x = float('-inf') if i == 0 else nums1[i - 1]
        min_right_x = float('inf') if i == x else nums1[i]
        max_left_y = float('-inf') if j == 0 else nums2[j - 1]
        min_right_y = float('inf') if j == y else nums2[j]
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            if (x + y) % 2 == 1:
                return max(max_left_x, max_left_y)
            else:
                return (max(max_left_x, max_left_y) + min(min_right_x, min_right_y)) / 2
        elif max_left_x > min_right_y:
            right = i - 1
        else:
            left = i + 1