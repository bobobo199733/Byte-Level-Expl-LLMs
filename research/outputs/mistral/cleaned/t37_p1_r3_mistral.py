class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def linked_list_cycle(head: ListNode) -> bool:
    if not head or not head.next:
        return False
    slow_ptr, fast_ptr = (head, head.next)
    while fast_ptr and fast_ptr.next:
        if slow_ptr == fast_ptr:
            return True
        slow_ptr = slow_ptr.next
        fast_ptr = fast_ptr.next.next
    return False