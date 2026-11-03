class Node:

    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinaryTree:

    def __init__(self, root=None):
        self.root = root

def binary_tree_inorder(tree):
    result = []

    def inorder_traversal(node):
        if node is not None:
            inorder_traversal(node.left)
            result.append(node.val)
            inorder_traversal(node.right)
    if tree.root is not None:
        inorder_traversal(tree.root)
    return result