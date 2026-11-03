def serialize_tree(root):
    if root is None:
        return 'None,'

    def helper(node):
        if node is None:
            return 'None,'
        return f"{node.val},{''.join((helper(child) for child in (node.left, node.right)))}"
    return helper(root)