import heapq

def merge_k_sorted_lists(lists):
    heap = []
    for list_ in lists:
        if list_:
            heapq.heappush(heap, (list_[0], list_, 0))
    result = []
    while heap:
        _, current_list, index = heapq.heappop(heap)
        result.append(current_list[index])
        index += 1
        if index < len(current_list):
            heapq.heappush(heap, (current_list[index], current_list, index))
    return result