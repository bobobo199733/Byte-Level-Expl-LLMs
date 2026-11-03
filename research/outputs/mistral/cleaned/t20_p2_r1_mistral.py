import heapq

def merge_k_sorted_lists(lists):
    if not lists:
        return []
    elif len(lists) == 1:
        return lists[0]
    minheap = []
    for list_ in lists:
        heapq.heappush(minheap, (len(list_), list_[0]))
    result = []
    while minheap:
        length, value = heapq.heappop(minheap)
        result.append(value)
        if len(result[-1]) > 0:
            heapq.heappush(minheap, (length - 1, result[-1][-1]))
    return result