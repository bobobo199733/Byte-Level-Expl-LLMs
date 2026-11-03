def binary_tree_inorder(tree):
    result = []

    def traverse(node):
        if node is None:
            return
        traverse(node['left'])
        result.append(node['val'])
        traverse(node['right'])
    traverse(tree)
    return result