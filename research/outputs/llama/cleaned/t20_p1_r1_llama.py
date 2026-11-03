import heapq

def merge_k_sorted_lists(lists):
    """
    Merge multiple sorted lists into one sorted list.

    Args:
        lists (list of lists): A list containing multiple sorted lists.

    Returns:
        list: A single sorted list containing all elements from the input lists.
    """
    merged_list = []
    min_heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))
    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        merged_list.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))
    return merged_list