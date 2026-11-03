class Node:
    """Node class representing a node in the linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None

def linked_list_cycle(head):
    """
    Determines whether a linked list contains a cycle.

    Args:
    head (Node): The head of the linked list.

    Returns:
    bool: True if a cycle exists, False otherwise.
    """
    if head is None or head.next is None:
        return False
    tortoise = head
    hare = head
    while True:
        if hare is None or hare.next is None:
            return False
        tortoise = tortoise.next
        hare = hare.next.next
        if tortoise == hare:
            return True