def median_of_two_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        return median_of_two_sorted_arrays(nums2, nums1)
    total_length = len(nums1) + len(nums2)
    half_length = total_length // 2
    left, right = (0, len(nums1) - 1)
    while True:
        i = (left + right) // 2
        j = half_length - i - 2
        nums1_left = nums1[i] if i >= 0 else float('-infinity')
        nums1_right = nums1[i + 1] if i + 1 < len(nums1) else float('infinity')
        nums2_left = nums2[j] if j >= 0 else float('-infinity')
        nums2_right = nums2[j + 1] if j + 1 < len(nums2) else float('infinity')
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            if total_length % 2 == 0:
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2.0
            else:
                return min(nums1_right, nums2_right)
        elif nums1_left > nums2_right:
            right = i - 1
        else:
            left = i + 1