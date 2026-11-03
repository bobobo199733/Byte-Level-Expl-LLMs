def binary_tree_inorder(tree):

    def inorder_traversal(node_index=0):
        if node_index >= len(tree):
            return []
        left_subtree = inorder_traversal(2 * node_index + 1)
        right_subtree = inorder_traversal(2 * node_index + 2)
        return left_subtree + [tree[node_index]] + right_subtree
    return inorder_traversal()