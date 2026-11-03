def build_tree(nodes):
    if not nodes:
        return None
    root = Node(nodes[0])
    root.left = build_tree([node for node in nodes[1::2] if node])
    root.right = build_tree([node for node in nodes[2::2] if node])
    return root

class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def binary_tree_inorder(tree):
    result = []
    if tree is not None:
        if tree.left:
            result += binary_tree_inorder(tree.left)
        result.append(tree.value)
        if tree.right:
            result += binary_tree_inorder(tree.right)
    return result