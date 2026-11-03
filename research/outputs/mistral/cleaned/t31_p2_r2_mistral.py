class Node:

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def serialize_tree(root):

    def _serialize_tree(node, serialized=[]):
        if node is None:
            serialized.append('N')
        else:
            serialized.append(str(node.val))
            serialized = _serialize_tree(node.left, serialized)
            serialized = _serialize_tree(node.right, serialized)
        return serialized
    if root is None:
        return ''
    return ' '.join(_serialize_tree(root))