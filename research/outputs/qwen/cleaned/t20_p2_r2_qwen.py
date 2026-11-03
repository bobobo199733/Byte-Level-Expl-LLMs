import heapq

def merge_k_sorted_lists(lists):
    non_empty_lists = [lst for lst in lists if lst]
    merged_list = []
    for lst in non_empty_lists:
        merged_list.extend(lst)
    return sorted(merged_list)