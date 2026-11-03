from heapq import heappush, heappop

def merge_k_sorted_lists(lists):
    min_heap = []
    for i, lst in enumerate(lists):
        if lst:
            heappush(min_heap, (lst[0], 0, i))
    result = []
    while min_heap:
        val, idx, list_index = heappop(min_heap)
        result.append(val)
        if idx + 1 < len(lists[list_index]):
            next_val = lists[list_index][idx + 1]
            heappush(min_heap, (next_val, idx + 1, list_index))
    return result