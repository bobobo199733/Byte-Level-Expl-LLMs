def median_of_two_sorted_arrays(nums1, nums2):
    total_len = len(nums1) + len(nums2)
    if total_len % 2 == 1:
        sorted_lists = merge_and_sort(nums1, nums2)
        left_index = (total_len - 1) // 2
        return sorted_lists[left_index]
    else:
        sorted_lists = merge_and_sort(nums1, nums2)
        middle_index = total_len // 2 - 1
        median1 = sorted_lists[middle_index]
        if middle_index + 1 < len(sorted_lists):
            median2 = sorted_lists[middle_index + 1]
        else:
            median2 = float('inf') if nums1[-1] > nums2[0] else -float('inf')
        return (median1 + median2) / 2

def merge_and_sort(nums1, nums2):
    merged_list = sorted(nums1 + nums2)
    return merged_list