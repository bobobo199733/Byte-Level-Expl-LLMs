def binary_tree_inorder(tree):
    """
    Performs an inorder traversal of a binary tree represented as a list.

    Args:
        tree (list): A list representing the binary tree, where each element is either a node value or another list for its children.

    Returns:
        list: The values in the tree in inorder sequence.

    Raises:
        ValueError: If the input tree is not valid.
    """
    if tree is None:
        raise ValueError('Input must be a list')

    def _inorder(node):
        if node is None:
            return []
        result = []
        stack = [node]
        while stack:
            current_node = stack.pop()
            if isinstance(current_node, int) or not isinstance(current_node, (list, tuple)):
                result.append(current_node)
            else:
                if len(current_node) > 2:
                    raise ValueError('Invalid tree: node must have at most two children')
                for child in reversed(current_node[1:]):
                    stack.append(child)
        return result
    return _inorder(tree)