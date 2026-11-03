class TreeNode:

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def serialize_tree(root):
    """
    Converts a binary tree into a string.

    The string is in the format of a pre-order traversal, with each node's value followed by a '#' character to indicate that it has children,
    and a 'X' character to indicate an empty child node.
    """

    def _serialize(node, current_string):
        if not node:
            return current_string + 'X#'
        return _serialize(node.left, current_string + str(node.val) + '#') + _serialize(node.right, current_string + str(node.val) + '#')
    return _serialize(root, '')