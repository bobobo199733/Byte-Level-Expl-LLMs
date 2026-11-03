import heapq

def merge_k_sorted_lists(lists):
    if not lists:
        return []
    min_heap = []
    heapq.heapify(min_heap)
    for list_ in lists:
        if list_:
            heapq.heappush(min_heap, (list_[0], 0, list_))
    result = []
    while min_heap:
        _, index, current_list = heapq.heappop(min_heap)
        result.append(current_list[index])
        index += 1
        if index < len(current_list):
            heapq.heappush(min_heap, (current_list[index], index, current_list))
    return result