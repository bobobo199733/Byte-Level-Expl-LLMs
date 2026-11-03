def binary_tree_inorder(tree):

    def _binary_tree_inorder(node, result):
        if node is None:
            return
        _binary_tree_inorder(node[1], result)
        result.append(node[0])
        _binary_tree_inorder(node[2], result)
    if not isinstance(tree, list) or len(tree) < 3:
        raise ValueError('Invalid binary tree representation')
    result = []
    _binary_tree_inorder(tree, result)
    return result