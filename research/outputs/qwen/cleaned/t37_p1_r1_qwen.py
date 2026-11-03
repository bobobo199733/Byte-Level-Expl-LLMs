class ListNode:

    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def linked_list_cycle(head):
    if head is None or head.next is None:
        return False
    slow = head
    fast = head.next
    while slow != fast:
        if fast is None or fast.next is None:
            return False
        slow = slow.next
        fast = fast.next.next
    return True