def find_kth_element(A, B, k):
    if len(A) > len(B):
        A, B = (B, A)
    if not A:
        return B[k]
    m, n = (len(A), len(B))
    i = 0
    j = k - (m - i)
    if i == m:
        return B[j]
    if j >= n:
        return A[i]
    a = A[i]
    b = B[j]
    if a > b:
        return find_kth_element(A, B[j + 1:], k - (j + 1))
    else:
        return find_kth_element(A[i + 1:], B, k - (i + 1))

def median_of_two_sorted_arrays(nums1, nums2):
    total_length = len(nums1) + len(nums2)
    if total_length % 2 == 1:
        return find_kth_element(nums1, nums2, total_length // 2 + 1)
    else:
        mid1 = find_kth_element(nums1, nums2, total_length // 2)
        mid2 = find_kth_element(nums1, nums2, total_length // 2 + 1)
        return (mid1 + mid2) / 2.0