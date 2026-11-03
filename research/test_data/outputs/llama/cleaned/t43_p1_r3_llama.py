def binary_tree_inorder(tree):
    """
    Performs an inorder traversal on a binary tree.

    Args:
        tree (list): A list representing a binary tree. Each element is either None (null),
                     or another list to represent left and right children, respectively.
    
    Returns:
        list: The values in the inorder traversal of the tree as a new list.
    """

    def _inorder_helper(node):
        """
        Helper function for recursion.

        Args:
            node (list): A sublist representing a single node in the binary tree.

        Yields:
            int or None: Values from the inorder traversal, or None when traversing through None values.
        """
        if node is not None:
            yield from _inorder_helper(node[0])
            yield node[1]
            yield from _inorder_helper(node[2])
    result = []
    for node in tree:
        if node is not None:
            result.extend(_inorder_helper(node))
    return result