class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root: TreeNode) -> str:
    if not root:
        return 'None,'
    result = str(root.val) + ','
    result += serialize_tree(root.left)
    result += serialize_tree(root.right)
    return result