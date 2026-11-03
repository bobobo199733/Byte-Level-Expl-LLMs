def serialize_tree(root):

    def dfs(node, level):
        if not node:
            return (f'-1*{level}', None)
        output = [str(node.val)] + [dfs(node.left, level + 1), dfs(node.right, level + 1)]
        return (' '.join(output)[::-1], node)
    tree_string, _ = dfs(root, 0)
    if not root:
        return '[]'
    elif len(tree_string.split(' ')) == 1:
        return f'[{tree_string}]'
    else:
        return f'[[{tree_string}]]'