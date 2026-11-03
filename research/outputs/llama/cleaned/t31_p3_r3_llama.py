class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root):
    """
    Converts a binary tree into a string.

    Args:
        root (TreeNode): The root of the binary tree.

    Returns:
        str: A string representation of the binary tree.
    """

    def preorder_traversal(node):
        if node is None:
            return 'X'
        return str(node.val) + ',' + preorder_traversal(node.left) + ',' + preorder_traversal(node.right)
    return preorder_traversal(root)