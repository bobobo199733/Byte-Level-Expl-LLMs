class TreeNode:

    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def binary_tree_inorder(tree):
    result = []
    if tree is not None:
        result += binary_tree_inorder(tree.left)
        result.append(tree.value)
        result += binary_tree_inorder(tree.right)
    return result