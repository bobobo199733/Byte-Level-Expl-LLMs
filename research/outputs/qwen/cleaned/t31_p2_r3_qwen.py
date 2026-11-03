class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root):
    if root is None:
        return 'None,'
    queue = [root]
    result = ''
    while queue:
        node = queue.pop(0)
        if node is not None:
            result += str(node.val) + ','
            queue.append(node.left if node.left else None)
            queue.append(node.right if node.right else None)
        else:
            result += 'None,'
    return result