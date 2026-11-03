def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] >= pivot:
            i += 1
            arr[i], arr[j] = (arr[j], arr[i])
    arr[i + 1], arr[high] = (arr[high], arr[i + 1])
    return i + 1

def kth_largest(nums, k):
    n = len(nums)
    if n < k:
        raise ValueError('K is greater than the number of elements in the list.')
    pivot_index = partition(nums, 0, n - 1)
    while pivot_index != k - 1:
        if pivot_index > k - 1:
            n -= pivot_index - (k - 1)
            nums = nums[:pivot_index - 1]
        else:
            first_k = nums[:k]
            return sorted(first_k, reverse=True)[-1] if k == len(first_k) else kth_largest(nums[k:], k - pivot_index)
        pivot_index = partition(nums, 0, n - 1)