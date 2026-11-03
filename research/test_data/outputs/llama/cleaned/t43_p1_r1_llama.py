def binary_tree_inorder(tree):
    """
    Performs an inorder traversal of a binary tree and returns the result as a list.

    Args:
        tree (list): A representation of the binary tree, where each element is either a value or another list representing a child subtree.

    Returns:
        list: The inorder traversal of the input binary tree.
    """
    result = []

    def traverse(subtree):
        if subtree is None:
            return
        traverse(subtree[0])
        result.append(subtree[1])
        traverse(subtree[2])
    traverse(tree)
    return result