def median_of_two_sorted_arrays(nums1, nums2):
    """
    Compute the median of two sorted integer arrays.

    Args:
        nums1 (list): The first sorted array.
        nums2 (list): The second sorted array.

    Returns:
        float: The median of the combined arrays.

    Time complexity: O(log(min(m, n)))
    """
    if not all((nums1[i] <= nums1[i + 1] for i in range(len(nums1) - 1))):
        raise ValueError('nums1 is not sorted')
    if not all((nums2[i] <= nums2[i + 1] for i in range(len(nums2) - 1))):
        raise ValueError('nums2 is not sorted')
    if len(nums1) == 0:
        return get_median(nums2)
    if len(nums2) == 0:
        return get_median(nums1)
    m, n = (len(nums1), len(nums2))
    if m > n:
        nums1, nums2 = (nums2, nums1)
        m, n = (n, m)
    left, right = (0, min(m, n))
    while left <= right:
        i = (left + right) // 2
        j = (m + n + 1) // 2 - i
        max_left_x = nums1[i - 1] if i != 0 else float('-inf')
        min_right_x = nums1[i] if i != m else float('inf')
        max_left_y = nums2[j - 1] if j != 0 else float('-inf')
        min_right_y = nums2[j] if j != n else float('inf')
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            if (m + n) % 2 == 0:
                return (max(max_left_x, max_left_y) + min(min_right_x, min_right_y)) / 2.0
            else:
                return float(min(min_right_x, min_right_y))
        elif max_left_x > min_right_y:
            right = i - 1
        else:
            left = i + 1

def get_median(nums):
    """
    Get the median of a single sorted array.

    Args:
        nums (list): The sorted array.

    Returns:
        float: The median of the array.
    """
    n = len(nums)
    if n % 2 == 0:
        return (nums[n // 2 - 1] + nums[n // 2]) / 2.0
    else:
        return float(nums[n // 2])