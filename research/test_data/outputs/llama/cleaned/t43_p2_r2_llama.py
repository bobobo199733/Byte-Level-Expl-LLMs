def binary_tree_inorder(tree):
    """
    Performs an inorder traversal of a binary tree.

    Args:
        tree (list): A list representing a binary tree, where each element is either None (representing an empty node) or a pair containing the value and children of a node.

    Returns:
        list: A list of node values in the order they were visited during the traversal.

    Raises:
        ValueError: If the input is not a valid binary tree.
    """

    def inorder_helper(tree, result):
        if tree is None or not isinstance(tree, (list, tuple)) or len(tree) != 3:
            raise ValueError('Invalid binary tree')
        node = tree[1]
        if node and node[0] is not None:
            inorder_helper(node[0], result)
        if node:
            result.append(node[1])
        if node and node[2] is not None:
            inorder_helper(node[2], result)
    result = []
    inorder_helper(tree, result)
    return result