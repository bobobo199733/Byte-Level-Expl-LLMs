import heapq

class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        return self.val < other.val

def merge_k_sorted_lists(lists):
    if not lists:
        return None
    heap = []
    for lst in lists:
        if lst:
            heapq.heappush(heap, lst)
    dummy = ListNode()
    current = dummy
    while heap:
        node = heapq.heappop(heap)
        if node.next:
            heapq.heappush(heap, node.next)
        current.next = node
        current = current.next
    return dummy.next

def create_linked_list(elements):
    if not elements:
        return None
    head = ListNode(elements[0])
    current = head
    for element in elements[1:]:
        current.next = ListNode(element)
        current = current.next
    return head

def print_linked_list(head):
    current = head
    while current:
        print(current.val, end=' -> ')
        current = current.next
    print('None')