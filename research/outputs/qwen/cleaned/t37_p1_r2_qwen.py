class ListNode:

    def __init__(self, x):
        self.val = x
        self.next = None

def linked_list_cycle(head):
    if head is None or head.next is None:
        return False
    slow = head
    fast = head.next
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    return False