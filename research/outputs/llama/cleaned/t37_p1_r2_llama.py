def linked_list_cycle(head):
    """
    Detects whether a linked list contains a cycle.

    Args:
        head: The head node of the linked list.

    Returns:
        True if a cycle exists, False otherwise.
    """
    tortoise = head
    hare = head
    while tortoise and hare and hare.next:
        tortoise = tortoise.next
        hare = hare.next.next
        if tortoise == hare:
            return True
    return False