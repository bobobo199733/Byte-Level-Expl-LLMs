class TreeNode:

    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def inorder_traversal(tree):
    if tree is not None:
        inorder_traversal(tree.left)
        print(tree.val, end=' ')
        inorder_traversal(tree.right)