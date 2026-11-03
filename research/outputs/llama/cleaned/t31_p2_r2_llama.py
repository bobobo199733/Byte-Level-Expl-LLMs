class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize_tree(root: 'TreeNode') -> str:
    """
    Serialize a binary tree into a string representation.

    This function uses a level-order traversal strategy to traverse the tree.
    It handles null or empty child nodes explicitly and preserves all node values and tree structure.
    The output allows reconstruction of the original tree.

    :param root: The root of the binary tree
    :return: A string representation of the binary tree
    """
    if not root:
        return ''
    queue = [(root.val, False)]
    result = []
    while queue:
        val, is_leaf = queue.pop(0)
        result.append(str(val))
        if root.left:
            queue.append((root.left.val, False))
        else:
            queue.append('#')
        if root.right:
            queue.append((root.right.val, False))
        else:
            queue.append('#')
    return ' '.join(result)

def deserialize_tree(serialized: str) -> TreeNode:
    if not serialized:
        return None
    nodes = serialized.split()
    i = 0
    root = TreeNode(int(nodes[i]))
    queue = [root]
    while i < len(nodes):
        node = queue.pop(0)
        val = int(nodes[i])
        i += 1
        if nodes[i] != '#':
            node.left = TreeNode(val)
            queue.append(node.left)
        i += 1
        if nodes[i] != '#':
            node.right = TreeNode(val)
            queue.append(node.right)
        i += 1
    return root