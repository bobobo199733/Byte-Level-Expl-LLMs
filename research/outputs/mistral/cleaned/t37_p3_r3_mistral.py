class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def linked_list_cycle(head: ListNode) -> bool:
    if not head or not head.next:
        return False
    slow_pointer, fast_pointer = (head, head.next)
    while fast_pointer and fast_pointer.next:
        if slow_pointer == fast_pointer:
            return True
        slow_pointer = slow_pointer.next
        fast_pointer = fast_pointer.next.next
    return False