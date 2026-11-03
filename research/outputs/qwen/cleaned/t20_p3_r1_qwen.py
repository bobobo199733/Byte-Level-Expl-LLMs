class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_sorted_lists(lists):
    if not lists or len(lists) == 0:
        return None
    import heapq
    min_heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst.val, i))
    dummy_head = ListNode(0)
    current = dummy_head
    while min_heap:
        val, index = heapq.heappop(min_heap)
        current.next = lists[index]
        current = current.next
        if lists[index].next:
            lists[index] = lists[index].next
            heapq.heappush(min_heap, (lists[index].val, index))
    return dummy_head.next

def print_linked_list(node):
    while node:
        print(node.val, end=' -> ')
        node = node.next
    print('None')