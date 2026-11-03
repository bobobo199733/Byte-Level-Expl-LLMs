class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root):
    if root is None:
        return '#'
    left_serialized = serialize_tree(root.left)
    right_serialized = serialize_tree(root.right)
    return f'{root.val},{left_serialized},{right_serialized}'