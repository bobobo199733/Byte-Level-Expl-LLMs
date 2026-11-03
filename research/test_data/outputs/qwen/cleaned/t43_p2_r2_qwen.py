def binary_tree_inorder(tree):
    if not isinstance(tree, list) or not tree:
        raise ValueError('Invalid input: tree must be a non-empty list')
    result = []

    def inorder_traverse(subtree):
        if len(subtree) < 3:
            return
        left_child_index = 2 * (subtree[0] - 1) + 1
        right_child_index = 2 * (subtree[0] - 1) + 2
        inorder_traverse(tree[left_child_index:left_child_index + subtree[1]])
        result.append(subtree[0])
        inorder_traverse(tree[right_child_index:right_child_index + subtree[2]])
    inorder_traverse(tree)
    return result