import heapq

def merge_k_sorted_lists(lists):
    """
    Combines multiple sorted lists into one sorted list.

    Args:
        lists (list): A list of sorted lists.

    Returns:
        list: A single sorted list containing all elements from the input lists.
    """
    min_heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))
    merged_list = []
    while min_heap:
        value, list_index, element_index = heapq.heappop(min_heap)
        merged_list.append(value)
        if element_index + 1 < len(lists[list_index]):
            heapq.heappush(min_heap, (lists[list_index][element_index + 1], list_index, element_index + 1))
    return merged_list