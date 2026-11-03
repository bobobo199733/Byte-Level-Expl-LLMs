class Node:

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def serialize_tree(root):
    if not root:
        return 'None'

    def dfs(node):
        if not node:
            return ''
        result = str(node.val) + ','
        result += dfs(node.left)
        result += dfs(node.right)
        return result
    return dfs(root)[1:-1]