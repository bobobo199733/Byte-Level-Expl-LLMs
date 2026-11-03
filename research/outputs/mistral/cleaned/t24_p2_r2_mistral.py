def heapq_kth_largest(nums, k):
    import heapq
    heap = sorted(set(nums), reverse=True)[:k]
    if len(heap) < k:
        raise ValueError(f'K ({k}) is greater than the number of elements in the list.')
    return heap[0]