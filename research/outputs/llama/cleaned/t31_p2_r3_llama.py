def serialize_tree(root):
    """
    Serializes a binary tree into a string representation.

    Args:
        root (Node): Root node of the binary tree.

    Returns:
        str: Serialized string representation of the binary tree.
    """
    if not root:
        return 'X,'
    serialized = []
    stack = [(root, False)]
    while stack:
        node, is_end_of_child_list = stack.pop()
        if not node:
            serialized.append('X')
        else:
            serialized.append(str(node.val))
            stack.append((node.right, False))
            if not is_end_of_child_list:
                stack.append((node.left, True))
    return ','.join(serialized)