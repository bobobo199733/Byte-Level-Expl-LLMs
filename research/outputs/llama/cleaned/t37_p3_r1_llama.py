def linked_list_cycle(head):
    """
    Checks if a linked list contains a cycle.

    Args:
        head (Node): The head of the linked list.

    Returns:
        bool: True if a cycle is detected, False otherwise.
    """
    tortoise = head
    hare = head
    while tortoise and hare and hare.next:
        tortoise = tortoise.next
        hare = hare.next.next
        if tortoise == hare:
            return True
    return False