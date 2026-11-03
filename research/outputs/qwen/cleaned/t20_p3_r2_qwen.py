import heapq

def merge_k_sorted_lists(lists):
    min_heap = []

    def push_with_index(heap, item, idx):
        heapq.heappush(heap, (item[0], idx, item))
    for i, lst in enumerate(lists):
        if lst:
            push_with_index(min_heap, (lst[0], i, [lst.pop(0)]))
    result = []
    while min_heap:
        _, idx, item_list = heapq.heappop(min_heap)
        result.append(item_list[-1])
        if lists[idx]:
            push_with_index(min_heap, (lists[idx][0], idx, [lists[idx].pop(0)] + item_list))
    return result