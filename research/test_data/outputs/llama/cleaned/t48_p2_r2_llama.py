def median_of_two_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = (nums2, nums1)
    if len(nums1) == 0:
        return (nums2[0] + nums2[-1]) / 2.0 if len(nums2) % 2 else nums2[len(nums2) // 2]
    left, right = (0, len(nums1))
    while left <= right:
        partition_x = (left + right) // 2
        partition_y = len(nums2) - int((len(nums1) + len(nums2)) / 2.0 - partition_x)
        max_left_x = float('-inf') if partition_x == 0 else nums1[partition_x - 1]
        min_right_x = float('inf') if partition_x == len(nums1) else nums1[partition_x]
        max_left_y = float('-inf') if partition_y == 0 else nums2[partition_y - 1]
        min_right_y = float('inf') if partition_y == len(nums2) else nums2[partition_y]
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            if (len(nums1) + len(nums2)) % 2 == 0:
                return (max(max_left_x, max_left_y) + min(min_right_x, min_right_y)) / 2.0
            else:
                return float(max_left_x > min_right_y and max_left_y > min_right_x and (max_left_x or max_left_y))
        elif max_left_x > min_right_y:
            right = partition_x - 1
        else:
            left = partition_x + 1