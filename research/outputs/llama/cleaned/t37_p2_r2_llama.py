class Node:
    """Simple node class for the linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None

def linked_list_cycle(head):
    """
    Detects whether a linked list contains a cycle.

    Args:
        head (Node): The head of the linked list.

    Returns:
        bool: True if a cycle exists, False otherwise.
    """
    if not head or not head.next:
        return False
    tortoise = head
    hare = head
    while True:
        if not hare or not hare.next:
            return False
        tortoise = tortoise.next
        hare = hare.next.next
        if tortoise == hare:
            return True