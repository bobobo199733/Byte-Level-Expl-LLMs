class ListNode:

    def __init__(self, value=0, next=None):
        self.val = value
        self.next = next

def linked_list_cycle(head: ListNode) -> bool:
    if not head or not head.next:
        return False
    slow = head
    fast = head.next
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    return False