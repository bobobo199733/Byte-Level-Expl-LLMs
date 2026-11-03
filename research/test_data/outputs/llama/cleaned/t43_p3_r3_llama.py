class TreeNode:
    """Represents a node in a binary tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def binary_tree_inorder(tree):
    """
    Performs an in-order traversal on the given binary tree and returns the result as a list.

    :param tree: The root node of the binary tree.
    :return: A list containing the values of the nodes in in-order traversal order.
    """
    result = []
    _inorder_helper(tree, result)
    return result

def _inorder_helper(node, result):
    """
    Helper function for performing an in-order traversal.

    :param node: The current node being visited.
    :param result: A list to store the values of the nodes in in-order traversal order.
    """
    if node:
        _inorder_helper(node.left, result)
        result.append(node.value)
        _inorder_helper(node.right, result)