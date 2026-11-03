import heapq

def merge_k_sorted_lists(lists):
    if not lists:
        return []
    min_heap = []
    for lst in lists:
        if len(lst) > 0:
            heapq.heappush(min_heap, (lst[0], lst, 0))
    result = []
    while min_heap:
        _, list_, index = heapq.heappop(min_heap)
        result.append(list_[index])
        if len(list_) > index + 1:
            heapq.heappush(min_heap, (list_[index + 1], list_, index + 1))
    return result