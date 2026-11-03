import heapq

def merge_k_sorted_lists(lists):
    """
    Combines multiple sorted lists into one sorted list.

    Args:
        lists (list): A list of lists, each containing integers that are already sorted.

    Returns:
        list: A new sorted list that contains all elements from the input lists.
    """
    min_heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(min_heap)
    merged_list = []
    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        merged_list.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            heapq.heappush(min_heap, (lists[list_idx][elem_idx + 1], list_idx, elem_idx + 1))
    return merged_list