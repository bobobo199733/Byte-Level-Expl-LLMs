class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def linked_list_cycle(head: ListNode) -> bool:
    if not head or not head.next:
        return False
    slow, fast = (head, head.next)
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False