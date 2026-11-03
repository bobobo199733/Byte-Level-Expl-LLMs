def binary_tree_inorder(tree):

    def _inorder(node, result):
        if node is None:
            return
        _inorder(node[1], result)
        result.append(node[0])
        _inorder(node[2], result)
    if not isinstance(tree, list) or len(tree) < 3 or any((isinstance(v, str) for v in tree)):
        raise ValueError('Invalid binary tree representation')
    result = []
    _inorder(tree, result)
    return result