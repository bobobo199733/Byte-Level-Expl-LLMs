def median_of_two_sorted_arrays(nums1, nums2):
    """
    Finds the median of two sorted arrays.

    Args:
        nums1 (list): The first sorted array.
        nums2 (list): The second sorted array.

    Returns:
        float: The median of the combined arrays.
    """
    nums1 = list(nums1)
    nums2 = list(nums2)
    merged_array = merge_sorted_arrays(nums1, nums2)
    n = len(merged_array)
    if n % 2 == 0:
        return (merged_array[n // 2 - 1] + merged_array[n // 2]) / 2.0
    else:
        return float(merged_array[n // 2])

def merge_sorted_arrays(nums1, nums2):
    """
    Merges two sorted arrays into one.

    Args:
        nums1 (list): The first sorted array.
        nums2 (list): The second sorted array.

    Returns:
        list: A new sorted array containing all elements from both input arrays.
    """
    result = []
    while nums1 and nums2:
        if nums1[0] < nums2[0]:
            result.append(nums1.pop(0))
        else:
            result.append(nums2.pop(0))
    result.extend(nums1)
    result.extend(nums2)
    return result