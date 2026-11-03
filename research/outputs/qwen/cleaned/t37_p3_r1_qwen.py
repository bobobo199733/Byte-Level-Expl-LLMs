class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def linked_list_cycle(head: ListNode) -> bool:
    if head is None or head.next is None:
        return False
    tortoise = head
    hare = head.next
    while hare and hare.next:
        if tortoise == hare:
            return True
        tortoise = tortoise.next
        hare = hare.next.next
    return False