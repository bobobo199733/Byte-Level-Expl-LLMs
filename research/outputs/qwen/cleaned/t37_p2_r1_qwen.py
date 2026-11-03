class ListNode:

    def __init__(self, x):
        self.val = x
        self.next = None

def linked_list_cycle(head: ListNode) -> bool:
    if head is None or head.next is None:
        return False
    tortoise = head
    hare = head.next
    while tortoise != hare:
        if hare is None or hare.next is None:
            return False
        tortoise = tortoise.next
        hare = hare.next.next
    return True