import heapq

def merge_k_sorted_lists(lists):
    """
    Merge k sorted lists into a single sorted list.

    Args:
        lists (list): A list containing sorted integer lists.

    Returns:
        list: A single sorted list containing all elements from the input lists.
    """
    if not lists:
        return []
    merged_list = []
    for lst in lists:
        if lst:
            merged_list.extend(lst)
    merged_list.sort()
    return merged_list

def merge_k_sorted_lists_custom_heap(lists):
    """
    Merge k sorted lists into a single sorted list.

    Args:
        lists (list): A list containing sorted integer lists.

    Returns:
        list: A single sorted list containing all elements from the input lists.
    """
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], 0, i))
    merged_list = []
    while heap:
        val, idx, list_idx = heapq.heappop(heap)
        merged_list.append(val)
        if idx + 1 < len(lists[list_idx]):
            heapq.heappush(heap, (lists[list_idx][idx + 1], idx + 1, list_idx))
    return merged_list