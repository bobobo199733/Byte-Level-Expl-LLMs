def serialize_tree(root):

    def pre_order(node):
        if not node:
            return 'None,'
        serialized = str(node) + ','
        serialized += pre_order(node.left)
        serialized += pre_order(node.right)
        return serialized
    result = pre_order(root)
    return '[' + result[:-1] + ']'