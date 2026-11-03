class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root):
    if root is None:
        return 'None,'
    serialized = str(root.val) + ','
    serialized += serialize_tree(root.left)
    serialized += serialize_tree(root.right)
    return serialized