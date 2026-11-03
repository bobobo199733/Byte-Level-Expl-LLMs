import heapq

def merge_k_sorted_lists(lists):
    merged = []
    min_heap = []
    for list_ in lists:
        if len(list_) > 0:
            heapq.heappush(min_heap, (list_[0], 0, list_))
    while min_heap:
        _, index, current_list = heapq.heappop(min_heap)
        value = current_list[index]
        merged.append(value)
        index += 1
        if len(current_list) > index < len(current_list):
            heapq.heappush(min_heap, (current_list[index], index, current_list))
    return merged