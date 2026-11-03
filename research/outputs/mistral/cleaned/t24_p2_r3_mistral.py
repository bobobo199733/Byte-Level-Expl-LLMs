def heapq_kth_largest(nums, k):
    import heapq
    if len(nums) < k:
        raise ValueError('K must be smaller than the length of the list')
    heap = sorted(nums)[:k]
    return heapq.nlargest(1, heap)[0]