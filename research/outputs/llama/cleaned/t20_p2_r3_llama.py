import heapq

def merge_k_sorted_lists(lists):
    """
    Merges k sorted lists into a single sorted list.

    Args:
        lists (list): A list of sorted integer lists.

    Returns:
        list: A single sorted list containing all elements from the input lists.
    """
    merged_list = []
    min_heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(min_heap)
    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        merged_list.append(val)
        if elem_idx < len(lists[list_idx]) - 1:
            heapq.heappush(min_heap, (lists[list_idx][elem_idx + 1], list_idx, elem_idx + 1))
    return merged_list