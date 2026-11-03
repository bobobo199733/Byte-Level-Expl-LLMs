class Node:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def binary_tree_inorder(node):
    result = []
    if node:
        result += binary_tree_inorder(node.left)
        result.append(node.data)
        result += binary_tree_inorder(node.right)
    return result