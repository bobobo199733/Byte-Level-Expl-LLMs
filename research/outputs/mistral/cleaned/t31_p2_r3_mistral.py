class TreeNode:

    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None

def serialize_tree(root):
    if not root:
        return 'None'
    queue = [root]
    result = []
    while queue:
        current_node = queue.pop(0)
        if current_node:
            result.append(str(current_node.val))
            queue.append(current_node.left)
            queue.append(current_node.right)
        else:
            result.append('None')
    return '[' + ', '.join(result) + ']'