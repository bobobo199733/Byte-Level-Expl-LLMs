import heapq

def merge_k_sorted_lists(lists):
    if not lists:
        return []
    elif len(lists) == 1:
        return lists[0]
    min_heap = []
    for lst in lists:
        if lst:
            heapq.heappush(min_heap, (lst[0], lst[1], lst))
    result = []
    while min_heap:
        _, value, list_ref = heapq.heappop(min_heap)
        result.append(value)
        if list_ref[1]:
            heapq.heappush(min_heap, (list_ref[0], list_ref[1].pop(0), list_ref))
    return result