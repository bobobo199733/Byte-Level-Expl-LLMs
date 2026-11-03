import heapq

def merge_k_sorted_lists(lists):
    if not lists:
        return []
    min_heap = []
    for list_ in lists:
        if list_ and len(min_heap) < len(lists):
            heapq.heappush(min_heap, (list_[0], 0, list_))
        elif list_ and len(min_heap) == len(lists):
            compared = False
            for _ in range(len(min_heap)):
                item, index, current_list = min_heap[0]
                if item > list_[0]:
                    heapq.heappop(min_heap)
                    break
                else:
                    compared = True
            if not compared:
                heapq.heappushpop(min_heap, (list_[0], 0, list_))
    result = []
    while min_heap:
        item, index, current_list = heapq.heappop(min_heap)
        result.append(item)
        if current_list and len(current_list) > 1:
            next_item = current_list[1]
            heapq.heappush(min_heap, (next_item, index, current_list))
    return result