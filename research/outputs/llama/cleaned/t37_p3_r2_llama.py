class Node:

    def __init__(self, value):
        self.value = value
        self.next = None

def linked_list_cycle(head):
    """
    Check if a linked list has a cycle.

    Args:
        head (Node): The head of the linked list.

    Returns:
        bool: True if the linked list has a cycle, False otherwise.
    """
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False