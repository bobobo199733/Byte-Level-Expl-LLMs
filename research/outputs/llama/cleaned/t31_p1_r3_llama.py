def serialize_tree(root):
    """
    Serializes a binary tree into a string.

    This function uses a pre-order traversal to create the serialized string, 
    which is a string of space-separated node values where # represents an empty subtree.

    :param root: The root node of the binary tree.
    :return: A string representing the serialized binary tree.
    """

    def serialize(node):
        if node:
            yield str(node.val)
            yield from serialize(node.left)
            yield from serialize(node.right)
        else:
            yield '#'
    return ' '.join(yield_from(serialize(root)))

class Node:

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right