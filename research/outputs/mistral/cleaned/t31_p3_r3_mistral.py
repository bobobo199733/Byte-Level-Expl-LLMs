class Node:

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def serialize_tree(root):
    if root is None:
        return '#'
    return str(root.val) + (',' + serialize_tree(root.left) if root.left else '') + (',' + serialize_tree(root.right) if root.right else '')