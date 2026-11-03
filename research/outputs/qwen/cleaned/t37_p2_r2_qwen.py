class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def linked_list_cycle(head: ListNode) -> bool:
    if not head or not head.next:
        return False
    tortoise = head
    hare = head.next
    while tortoise != hare:
        if not hare or not hare.next:
            return False
        tortoise = tortoise.next
        hare = hare.next.next
    return True