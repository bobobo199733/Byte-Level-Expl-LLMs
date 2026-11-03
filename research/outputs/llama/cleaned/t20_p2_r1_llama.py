import heapq

def merge_k_sorted_lists(lists):
    """
    Merges k sorted lists into a single sorted list.

    Args:
        lists (list): A list containing k sorted integer lists.

    Returns:
        list: The merged sorted list of integers.
    """
    if not lists:
        return []
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]
    heapq.heapify(heap)
    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    return result