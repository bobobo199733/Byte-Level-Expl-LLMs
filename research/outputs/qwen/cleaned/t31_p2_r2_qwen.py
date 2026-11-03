class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root):
    if root is None:
        return 'None,'
    result = str(root.val) + ','
    if root.left is not None:
        result += serialize_tree(root.left)
    else:
        result += 'None,'
    if root.right is not None:
        result += serialize_tree(root.right)
    else:
        result += 'None,'
    return result