class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def binary_tree_inorder(tree):
    if tree is None:
        return []
    inorder_left = binary_tree_inorder(tree.left)
    root_val = [tree.val]
    inorder_right = binary_tree_inorder(tree.right)
    return inorder_left + root_val + inorder_right