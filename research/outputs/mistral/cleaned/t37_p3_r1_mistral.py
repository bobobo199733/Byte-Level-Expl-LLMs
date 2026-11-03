class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def get_length(head: ListNode) -> int:
    count = 0
    current = head
    while current is not None:
        count += 1
        current = current.next
    return count

def linked_list_cycle(head: ListNode) -> bool:
    if not head or not head.next:
        return False
    fast = head.next
    slow = head
    length = get_length(head)
    for _ in range(1, length + 1):
        if fast is None or fast.next is None:
            return False
        fast = fast.next.next
        slow = slow.next
        if fast == slow:
            return True
    return False