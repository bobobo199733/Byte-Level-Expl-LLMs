import heapq

def merge_k_sorted_lists(lists):
    heap = []
    for list_ in lists:
        if list_:
            heapq.heappush(heap, (min(list_), list_, 0))
    result = []
    while heap:
        _, curr_list, index = heapq.heappop(heap)
        result.append(curr_list[index])
        index += 1
        if index < len(curr_list):
            heapq.heappush(heap, (min(curr_list[index:]), curr_list, index))
    return result