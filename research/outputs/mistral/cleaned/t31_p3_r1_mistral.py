class Node:

    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def serialize_tree(root):

    def dfs(node, result):
        if node is None:
            result.append('#')
            return
        result.append(str(node.val))
        dfs(node.left, result)
        dfs(node.right, result)
    result = []
    dfs(root, result)
    return ' '.join(result)