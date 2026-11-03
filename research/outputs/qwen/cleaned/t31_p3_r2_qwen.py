class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root: TreeNode) -> str:
    if not root:
        return 'None'
    left_str = serialize_tree(root.left)
    right_str = serialize_tree(root.right)
    serialized = f'{root.val},{left_str},{right_str}'
    return serialized