class Node:

    def __init__(self, value):
        self.value = value
        self.next = None

def linked_list_cycle(head):
    """
    Determines if a singly-linked list contains a cycle.
    
    Args:
        head (Node): The head node of the linked list.
        
    Returns:
        bool: True if the linked list has a cycle, False otherwise.
    """
    if not head or not head.next:
        return False
    slow = head
    fast = head
    while True:
        slow = slow.next
        if not fast or not fast.next:
            return False
        fast = fast.next.next
        if slow == fast:
            return True