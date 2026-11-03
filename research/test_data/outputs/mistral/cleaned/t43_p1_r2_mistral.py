def binary_tree_inorder(tree):
    result = []

    def _traverse(node):
        if not node:
            return
        _traverse(node[1])
        result.append(node[0])
        _traverse(node[2])
    _traverse(tree)
    return result