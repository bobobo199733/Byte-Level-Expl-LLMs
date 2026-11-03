def merge_k_sorted_lists(lists):
    if len(lists) <= 1:
        return lists
    mid = len(lists) // 2
    left_half = lists[:mid]
    right_half = lists[mid:]
    left = merge_k_sorted_lists(left_half)
    right = merge_k_sorted_lists(right_half)
    return merge_two_sorted_lists(left, right)

def merge_two_sorted_lists(list1, list2):
    merged_list = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1
    merged_list += list1[i:]
    merged_list += list2[j:]
    return merged_list