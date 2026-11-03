def binary_tree_inorder(tree):

    def inorder_traverse(node_index, result):
        if 2 * node_index + 1 >= len(tree):
            return
        inorder_traverse(2 * node_index + 1, result)
        result.append(tree[node_index])
        inorder_traverse(2 * node_index + 2, result)
    result = []
    inorder_traverse(0, result)
    return result