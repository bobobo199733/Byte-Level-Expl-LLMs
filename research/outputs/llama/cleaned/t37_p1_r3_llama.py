def linked_list_cycle(head):
    """
    Detects whether a linked list contains a cycle.

    Args:
        head (Node): The head of the linked list.

    Returns:
        bool: True if a cycle exists, False otherwise.
    """
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False