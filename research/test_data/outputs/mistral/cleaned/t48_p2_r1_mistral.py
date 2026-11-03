def median_of_two_sorted_arrays(nums1, nums2):
    m, n = (len(nums1), len(nums2))

    def merge_and_sort(arr1, arr2):
        return sorted(arr1 + arr2)
    total_len = m + n
    if total_len == 0:
        return float('NaN')
    if total_len & 1:
        partition_idx = (total_len - 1) // 2
        arr1, arr2 = merge_and_sort(nums1[:partition_idx], nums2[:partition_idx + 1])
    else:
        partition_idx = total_len // 2
        arr1, arr2 = merge_and_sort(nums1[:partition_idx], nums2[:partition_idx])
    if m > n:
        arr1, arr2 = (arr2, arr1)
        m, n = (n, m)
    partition_val = binary_search(arr1, arr2[0], arr2[-1])
    left_side = []
    right_side = []
    for i in range(len(arr1)):
        if arr1[i] < partition_val:
            left_side.append(arr1[i])
        else:
            right_side.append(arr1[i])
    if binary_search(nums2, partition_val, nums2[-1]) >= partition_idx:
        return partition_val
    else:
        while len(left_side) < partition_idx:
            left_side.append(nums2[0])
            nums2 = nums2[1:]
        return left_side[-1]

def binary_search(arr, low, high):
    if len(arr) == 0:
        return float('NaN')
    if low <= high:
        mid = (low + high) // 2
        if arr[mid] == mid:
            return mid
        elif arr[mid] < mid:
            return binary_search(arr, mid + 1, high)
        else:
            return binary_search(arr, low, mid - 1)
    else:
        return float('NaN')