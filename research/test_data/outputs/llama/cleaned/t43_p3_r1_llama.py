class Node:
    """Represents a node in the binary tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def binary_tree_inorder(tree):
    """
    Performs an inorder traversal of the binary tree and returns the result as a list.

    :param tree: The root node of the binary tree.
    :return: A list containing the values of the nodes in inorder.
    """

    def _inorder_helper(node, result):
        if node:
            _inorder_helper(node.left, result)
            result.append(node.value)
            _inorder_helper(node.right, result)
    result = []
    _inorder_helper(tree, result)
    return result