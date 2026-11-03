class TreeNode:

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def serialize_tree(root):
    """
    Serialize a binary tree into a string.

    Args:
        root (TreeNode): The root of the binary tree.

    Returns:
        str: A string representation of the binary tree.
    """

    def _serialize(node, result):
        if node is None:
            return result + 'X,'
        result += str(node.val) + ','
        result = _serialize(node.left, result)
        result = _serialize(node.right, result)
        return result
    return _serialize(root, '')