def binary_tree_inorder(tree):
    """
    Performs an inorder traversal of a binary tree represented as a list.

    Args:
        tree (list): A binary tree represented as a nested list where each element is either a value or another list.
        
    Returns:
        list: The node values in inorder sequence.

    Raises:
        ValueError: If the input tree is invalid.
    """

    def helper(node):
        if not isinstance(node, list) or len(node) != 3 or (not all((isinstance(child, (list, int)) for child in node))):
            raise ValueError('Invalid tree')
        return [val for val in binary_tree_inorder(node[1]) + [node[0]] + binary_tree_inorder(node[2])] if node else []
    if isinstance(tree, list) and len(tree) == 3:
        return helper(tree)
    elif isinstance(tree, (int, float)):
        return [tree]
    else:
        raise ValueError('Invalid tree')