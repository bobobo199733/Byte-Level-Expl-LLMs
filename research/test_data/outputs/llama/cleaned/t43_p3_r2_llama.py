class Node:
    """Represents a node in the binary tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def binary_tree_inorder(tree):
    """
    Returns the inorder traversal of a binary tree.

    :param tree: The root node of the binary tree.
    :return: A list containing the values in the order they were visited.
    """
    result = []
    _inorder_helper(tree, result)
    return result

def _inorder_helper(node, result):
    """Recursive helper function to perform inorder traversal."""
    if node:
        _inorder_helper(node.left, result)
        result.append(node.value)
        _inorder_helper(node.right, result)