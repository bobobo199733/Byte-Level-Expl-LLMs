import heapq

class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_sorted_lists(lists):
    iterators = [iter(lst) for lst in lists]
    merged_list = []
    min_heap = [(next(it, None), i, it) for i, it in enumerate(iterators) if next(it, None) is not None]
    heapq.heapify(min_heap)
    while min_heap:
        val, index, iterator = heapq.heappop(min_heap)
        merged_list.append(val)
        try:
            next_val = next(iterator)
            heapq.heappush(min_heap, (next_val, index, iterator))
        except StopIteration:
            pass
    return merged_list

def create_linked_list(values):
    head = ListNode()
    current = head
    for value in values:
        current.next = ListNode(value)
        current = current.next
    return head.next if head else None

def linked_list_to_list(node):
    result = []
    while node is not None:
        result.append(node.val)
        node = node.next
    return result