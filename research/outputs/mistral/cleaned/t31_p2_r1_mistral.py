class Node:

    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root):
    if root is None:
        return 'N'

    def _serialize_helper(node, level=0):
        result = str(node.val) + '#' * (32 - level) if node else '.' + '#' * 32
        if node and node.left:
            result += '\n' + _serialize_helper(node.left, level + 1)
        elif node is None:
            result += '\n# ' + '#' * (32 - level + 1)
        if node and node.right:
            result += _serialize_helper(node.right, level + 1) + '\n'
        return result
    return _serialize_helper(root)