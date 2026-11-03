def serialize_tree(root):
    """
    Serialize a binary tree into a string.

    :param root: The root of the binary tree.
    :return: A string representation of the binary tree.
    """

    def dfs(node, res):
        if not node:
            res.append('X')
            return
        res.append(str(node.val))
        dfs(node.left, res)
        dfs(node.right, res)
    res = []
    dfs(root, res)
    return ','.join(res)