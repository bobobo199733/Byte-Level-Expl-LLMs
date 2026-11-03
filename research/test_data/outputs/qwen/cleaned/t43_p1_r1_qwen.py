def binary_tree_inorder(tree):

    def inorder_helper(index):
        if index >= len(tree) or tree[index] is None:
            return []
        left_subtree = inorder_helper(2 * index + 1)
        value = [tree[index]] if tree[index] is not None else []
        right_subtree = inorder_helper(2 * index + 2)
        return left_subtree + value + right_subtree
    if tree:
        return inorder_helper(0)
    else:
        return []